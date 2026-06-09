"""Build sample-lock action plans from readiness and manual review evidence."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlparse, urlunparse


@dataclass(frozen=True)
class SampleLockPlanRow:
    url: str
    name: str
    category: str
    cohort: str
    readiness_status: str
    worksheet_decision: str
    lock_status: str
    priority: int
    next_action: str
    access_screenshot_path: str
    capture_screenshot_ref: str
    capture_dom_snapshot_ref: str
    lock_notes: str


FIELDNAMES = list(SampleLockPlanRow.__dataclass_fields__.keys())
QUEUE_FIELDNAMES = ["queue_name", *FIELDNAMES]
WEEKLY_TARGET_FIELDNAMES = [
    "url",
    "name",
    "category",
    "inherited_from_phd_mentor",
    "notes",
]
QUEUE_SPECS = {
    "weekly_capture_shortlist": {
        "provisionally_selected",
        "selected_for_deep_sample",
        "selected_no_banner_case",
    },
    "manual_review_queue": {"pending_manual_review"},
    "rerun_capture_queue": {"needs_capture_rerun", "needs_access_probe"},
    "replacement_review_queue": {
        "blocked_review_or_replace",
        "replacement_needed",
    },
    "optional_control_queue": {"optional_control"},
}


def build_sample_lock_plan(
    readiness_csv: Path,
    worksheet_csv: Path,
) -> list[SampleLockPlanRow]:
    worksheet_rows = _read_latest_by_url(worksheet_csv)
    rows: list[SampleLockPlanRow] = []

    with readiness_csv.open(encoding="utf-8") as fh:
        for readiness in csv.DictReader(fh):
            url = (readiness.get("url") or "").strip()
            if not url:
                continue
            worksheet = worksheet_rows.get(_canonicalize_url(url), {})
            worksheet_decision = (worksheet.get("sample_decision") or "").strip()
            lock_status, priority, next_action = _classify_lock_status(
                readiness_status=(readiness.get("readiness_status") or "").strip(),
                worksheet_decision=worksheet_decision,
            )
            rows.append(
                SampleLockPlanRow(
                    url=url,
                    name=(readiness.get("name") or "").strip(),
                    category=(readiness.get("category") or "").strip(),
                    cohort=(readiness.get("cohort") or "").strip(),
                    readiness_status=(
                        readiness.get("readiness_status") or ""
                    ).strip(),
                    worksheet_decision=worksheet_decision,
                    lock_status=lock_status,
                    priority=priority,
                    next_action=next_action,
                    access_screenshot_path=(
                        readiness.get("access_screenshot_path")
                        or worksheet.get("access_screenshot_path")
                        or ""
                    ).strip(),
                    capture_screenshot_ref=(
                        worksheet.get("capture_screenshot_ref") or ""
                    ).strip(),
                    capture_dom_snapshot_ref=(
                        worksheet.get("capture_dom_snapshot_ref") or ""
                    ).strip(),
                    lock_notes=_lock_notes(readiness, worksheet),
                )
            )
    return rows


def export_sample_lock_plan_to_csv(
    out_csv: Path,
    rows: list[SampleLockPlanRow],
) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            record = asdict(row)
            record["priority"] = str(row.priority)
            writer.writerow(record)


def summarize_sample_lock_plan(rows: list[SampleLockPlanRow]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for row in rows:
        summary[row.lock_status] = summary.get(row.lock_status, 0) + 1
    return summary


def export_sample_lock_queues(
    lock_plan_csv: Path,
    out_dir: Path,
) -> dict[str, int]:
    """Split a sample-lock plan into next-action queue CSV files."""
    rows = _read_lock_plan_rows(lock_plan_csv)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, int] = {}

    for queue_name, lock_statuses in QUEUE_SPECS.items():
        queue_rows = [
            row for row in rows if row.get("lock_status", "").strip() in lock_statuses
        ]
        manifest[queue_name] = len(queue_rows)
        _write_queue_csv(out_dir / f"{queue_name}.csv", queue_name, queue_rows)

    _write_manifest(out_dir / "queue_manifest.csv", manifest)
    return manifest


def export_weekly_targets_from_queues(
    queues_dir: Path,
    out_csv: Path,
) -> int:
    """Create a site-list CSV for the next weekly capture from action queues."""
    rows = _read_queue_rows(queues_dir / "weekly_capture_shortlist.csv")
    rows.extend(_read_queue_rows(queues_dir / "rerun_capture_queue.csv"))
    target_rows = _deduplicate_targets(rows)

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=WEEKLY_TARGET_FIELDNAMES)
        writer.writeheader()
        for row in target_rows:
            writer.writerow(
                {
                    "url": row["url"],
                    "name": row["name"],
                    "category": row["category"],
                    "inherited_from_phd_mentor": "false",
                    "notes": f"{row['queue_name']}: {row['next_action']}",
                }
            )
    return len(target_rows)


def _read_latest_by_url(path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            url = (row.get("url") or "").strip()
            if url:
                rows[_canonicalize_url(url)] = row
    return rows


def _read_queue_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as fh:
        return [
            row
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        ]


def _deduplicate_targets(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    targets: list[dict[str, str]] = []
    for row in rows:
        url = (row.get("url") or "").strip()
        canonical_url = _canonicalize_url(url)
        if not canonical_url or canonical_url in seen:
            continue
        seen.add(canonical_url)
        targets.append(
            {
                "queue_name": (row.get("queue_name") or "").strip(),
                "url": url,
                "name": (row.get("name") or "").strip(),
                "category": (row.get("category") or "").strip(),
                "next_action": (row.get("next_action") or "").strip(),
            }
        )
    return targets


def _read_lock_plan_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as fh:
        return [
            row
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        ]


def _write_queue_csv(
    out_csv: Path,
    queue_name: str,
    rows: list[dict[str, str]],
) -> None:
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=QUEUE_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({"queue_name": queue_name, **row})


def _write_manifest(out_csv: Path, manifest: dict[str, int]) -> None:
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["queue_name", "row_count"])
        writer.writeheader()
        for queue_name, row_count in manifest.items():
            writer.writerow({"queue_name": queue_name, "row_count": str(row_count)})


def _classify_lock_status(
    *,
    readiness_status: str,
    worksheet_decision: str,
) -> tuple[str, int, str]:
    if worksheet_decision == "keep_consent_sample":
        return (
            "selected_for_deep_sample",
            1,
            "include in deep-sample weekly capture",
        )
    if worksheet_decision == "keep_no_banner_case":
        return (
            "selected_no_banner_case",
            1,
            "include only if no-banner comparison is useful and labeled clearly",
        )
    if worksheet_decision == "rerun_fresh_context":
        return (
            "needs_capture_rerun",
            2,
            "rerun weekly capture with fresh context or longer timeout",
        )
    if worksheet_decision == "replace_candidate":
        return ("replacement_needed", 3, "replace with a comparable accessible site")
    if worksheet_decision == "exclude":
        return ("excluded", 5, "exclude from deep sample")

    if readiness_status == "pilot_ready":
        return (
            "provisionally_selected",
            1,
            "include in shortlist and continue weekly capture",
        )
    if readiness_status == "needs_cmp_review":
        return ("pending_manual_review", 2, "fill CMP review worksheet before sample lock")
    if readiness_status == "needs_weekly_capture":
        return (
            "needs_capture_rerun",
            2,
            "rerun weekly capture with fresh context or longer timeout",
        )
    if readiness_status == "control_candidate":
        return ("optional_control", 4, "keep only if a no-banner control is needed")
    if readiness_status == "access_blocked":
        return (
            "blocked_review_or_replace",
            3,
            "review access feasibility; replace unless kept as blocked canary",
        )
    if readiness_status == "needs_access_probe":
        return ("needs_access_probe", 2, "run access probe before sample lock")
    return ("needs_review", 3, "review readiness evidence before sample lock")


def _lock_notes(
    readiness: dict[str, str],
    worksheet: dict[str, str],
) -> str:
    reviewer_notes = (worksheet.get("reviewer_notes") or "").strip()
    if reviewer_notes:
        return reviewer_notes
    return (readiness.get("readiness_notes") or "").strip()


def _canonicalize_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", parsed.query, ""))
