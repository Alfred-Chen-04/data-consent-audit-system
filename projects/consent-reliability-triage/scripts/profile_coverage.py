"""Profile the three pinned source snapshots, without ranking candidates."""
import collections
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "evidence/sources"


def profile(path):
    duplicate_keys = []

    def pairs_hook(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                duplicate_keys.append(key)
            result[key] = value
        return result

    raw = path.read_bytes()
    data = json.loads(raw, object_pairs_hook=pairs_hook)
    rows = [(rule, region, value) for rule, regions in data.items()
            for region, value in regions.items()]
    fields = sorted({key for _, _, value in rows for key in value})
    field_profile = {}
    for key in fields:
        values = [v[key] for _, _, v in rows if key in v]
        item = {"present": len(values), "missing": len(rows) - len(values),
                "null": sum(v is None for v in values),
                "types": dict(collections.Counter(type(v).__name__ for v in values))}
        if all(type(v) is int for v in values):
            item.update(min=min(values), max=max(values),
                        nonzero=sum(v != 0 for v in values), negative=sum(v < 0 for v in values))
        if all(isinstance(v, list) for v in values):
            item.update(empty=sum(not v for v in values), max_length=max(map(len, values)),
                        duplicate_items=sum(len(v) - len(set(v)) for v in values),
                        invalid_urls=sum(not isinstance(u, str) or
                                         urlparse(u).scheme not in ("http", "https") or
                                         not urlparse(u).hostname for v in values for u in v))
        field_profile[key] = item
    regions = {}
    for region in sorted({g for _, g, _ in rows}):
        group = [v for _, g, v in rows if g == region]
        regions[region] = {"rows": len(group),
                           "errors_sum_not_unique_sites": sum(v.get("errors", 0) for v in group),
                           "selfTestFailures_sum_not_unique_sites": sum(v.get("selfTestFailures", 0) for v in group),
                           "error_positive_rows": sum(v.get("errors", 0) > 0 for v in group),
                           "selftest_positive_rows": sum(v.get("selfTestFailures", 0) > 0 for v in group)}
    mapped_urls = collections.defaultdict(set)
    for rule, region, value in rows:
        for field, urls in value.items():
            if isinstance(urls, list):
                for url in urls:
                    mapped_urls[url].add((rule, region, field))
    return data, {"file": path.name, "sha256": hashlib.sha256(raw).hexdigest(),
                  "rules": len(data), "rows": len(rows), "duplicate_json_keys": duplicate_keys,
                  "regions": regions, "fields": field_profile,
                  "rules_missing_some_regions": sum(len(v) < 3 for v in data.values()),
                  "unique_example_urls_across_all_lists": len(mapped_urls),
                  "urls_in_multiple_rule_region_field_locations": sum(len(v) > 1 for v in mapped_urls.values()),
                  "errors_gt_sites": [(r, g) for r, g, v in rows if v["errors"] > v["sites"]],
                  "selftest_failures_gt_sites": [(r, g) for r, g, v in rows if v["selfTestFailures"] > v["sites"]],
                  "errors_and_failing_list_overlap": [{"rule": r, "region": g,
                                                       "urls": sorted(set(v["errorSites"]) & set(v["failingSites"]))}
                                                      for r, g, v in rows if set(v["errorSites"]) & set(v["failingSites"])],
                  "bandcamp_example": data.get("bandcamp.com")}


def main():
    manifest = json.loads((SOURCES / "manifest.json").read_text())
    entries = [f for f in manifest["files"] if f["source_path"] == "data/coverage.json"]
    snapshots, data = [], []
    for entry in entries:
        content, result = profile(SOURCES / entry["file"])
        assert result["sha256"] == entry["sha256"], "Source hash mismatch"
        result["commit_time_not_collection_time"] = entry["last_change_commit_time"]
        snapshots.append(result)
        data.append(content)
    comparisons = []
    for i in range(len(data) - 1):
        newer, older = data[i], data[i + 1]
        new_keys = {(r, g) for r, gs in newer.items() for g in gs}
        old_keys = {(r, g) for r, gs in older.items() for g in gs}
        comparisons.append({"newer": entries[i]["file"], "older": entries[i + 1]["file"],
                            "common_rule_region_keys": len(new_keys & old_keys),
                            "added_keys": sorted(new_keys - old_keys),
                            "removed_keys": sorted(old_keys - new_keys),
                            "comparability": "key overlap only; crawl environment and rule equivalence not established"})
    output = ROOT / "evidence/schema_profile.json"
    output.write_text(json.dumps({"snapshots": snapshots, "comparisons": comparisons}, indent=2) + "\n")
    print(json.dumps({"output": str(output), "snapshots": [
        {k: s[k] for k in ("file", "rules", "rows", "regions")} for s in snapshots]}, indent=2))


if __name__ == "__main__":
    main()
