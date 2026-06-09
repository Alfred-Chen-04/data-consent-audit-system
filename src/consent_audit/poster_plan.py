"""Generate an SSRP poster storyboard from current research evidence."""

from __future__ import annotations

import csv
from pathlib import Path
from urllib.parse import urlparse, urlunparse


def export_ssrp_poster_plan(
    *,
    targets_csv: Path,
    audit_summary_csv: Path,
    longitudinal_summary_csv: Path,
    cmp_confirmation_csv: Path,
    results_tables_md: Path,
    paper_skeleton_md: Path,
    figure_plan_md: Path,
    writing_pack_md: Path,
    claim_register_md: Path,
    cycle_report_md: Path,
    out_md: Path,
    title: str,
    week_label: str,
) -> str:
    """Write a poster-specific storyboard, asset list, and finalization checklist."""

    targets = _read_rows(targets_csv)
    reports = _latest_by_url(_read_rows(audit_summary_csv), date_key="captured_at")
    summaries = _latest_by_url(_read_rows(longitudinal_summary_csv), date_key="week_of")
    confirmation_counts = _count_values(
        _read_rows(cmp_confirmation_csv),
        "confirmation_status",
        default="pending",
    )
    cycle_status = _extract_capture_status(cycle_report_md)
    text = _render_poster_plan(
        title=title,
        week_label=week_label,
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        cmp_confirmation_csv=cmp_confirmation_csv,
        results_tables_md=results_tables_md,
        paper_skeleton_md=paper_skeleton_md,
        figure_plan_md=figure_plan_md,
        writing_pack_md=writing_pack_md,
        claim_register_md=claim_register_md,
        cycle_report_md=cycle_report_md,
        targets=targets,
        reports=reports,
        summaries=summaries,
        confirmation_counts=confirmation_counts,
        cycle_status=cycle_status,
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")
    return text


def _render_poster_plan(
    *,
    title: str,
    week_label: str,
    targets_csv: Path,
    audit_summary_csv: Path,
    longitudinal_summary_csv: Path,
    cmp_confirmation_csv: Path,
    results_tables_md: Path,
    paper_skeleton_md: Path,
    figure_plan_md: Path,
    writing_pack_md: Path,
    claim_register_md: Path,
    cycle_report_md: Path,
    targets: list[dict[str, str]],
    reports: dict[str, dict[str, str]],
    summaries: dict[str, dict[str, str]],
    confirmation_counts: dict[str, int],
    cycle_status: str,
) -> str:
    target_count = len(targets)
    rq1_count = sum(1 for target in targets if _row_for(target, reports))
    rq2_count = sum(1 for target in targets if _row_for(target, summaries))
    category_counts = _count_values(targets, "category", default="unknown")
    tier_counts = _count_target_values(targets, reports, "tier", default="missing")
    banner_counts = _count_banner_classes(targets, reports)
    banner_tier_counts = _count_banner_present_values(targets, reports, "tier")
    no_visible_count = banner_counts.get("no_visible_banner", 0)
    severity_counts = _count_target_values(targets, summaries, "severity", default="missing")
    cmp_status = _format_counts(confirmation_counts) or "none"
    claim_status = _poster_claim_status(cycle_status)
    evidence_candidate = _evidence_card_candidate(targets, reports)
    timeline_candidates = _timeline_candidates(targets, summaries)
    timeline_source = _timeline_source(timeline_candidates)
    timeline_status = _timeline_status(cycle_status)
    poster_limitation = _poster_limitation(cycle_status)
    before_final_poster = _before_final_poster_items(cycle_status)

    return (
        f"# {title}\n\n"
        "## Evidence Snapshot\n\n"
        f"- Evidence window: {week_label}\n"
        f"- Target sites: {target_count}\n"
        f"- Categories: {_format_counts(category_counts) or 'none'}\n"
        f"- RQ1 poster data available: {rq1_count}/{target_count}\n"
        f"- RQ2 poster data available: {rq2_count}/{target_count}\n"
        f"- Banner evidence classes: {_format_counts(banner_counts) or 'none'}\n"
        f"- Banner-present automated tiers: {_format_counts(banner_tier_counts) or 'none'}\n"
        f"- Raw automated target tiers: {_format_counts(tier_counts) or 'none'}\n"
        f"- Latest longitudinal severity: {_format_counts(severity_counts) or 'none'}\n"
        f"- CMP confirmations: {cmp_status}\n"
        f"- Cycle capture status: `{cycle_status}`\n"
        f"- Poster claim status: {claim_status}\n\n"
        "## Poster Storyboard\n\n"
        "| Panel | Location | Content |\n"
        "|---|---|---|\n"
        "| Title and thesis | Top band | Show the system as a research audit, not a compliance product. |\n"
        "| Research questions | Left column | RQ1: score consent interfaces; RQ2: capture/version changes over time. |\n"
        "| Pipeline | Center column | Browser capture -> Layer scoring -> AuditReport -> WeeklySummary. |\n"
        "| Three-layer scoring | Center column | Path availability, path effort, transparency/unbiased choice. |\n"
        "| RQ1 evidence | Results band | Banner-present automated tiers: "
        f"{_format_counts(banner_tier_counts) or 'none'}; "
        f"no-visible-banner contrast candidates: {no_visible_count}. |\n"
        f"| RQ2 timeline | Results band | Current longitudinal severity: {_format_counts(severity_counts) or 'none'}. |\n"
        f"| Limitations | Bottom band | pending CMP/manual-review confirmations remain unresolved: {cmp_status}. |\n"
        "| Takeaway | Footer | Deep longitudinal evidence beats broad shallow claims. |\n\n"
        "## Figure Assets\n\n"
        "| Asset | Status | Source | Poster use |\n"
        "|---|---|---|---|\n"
        "| System pipeline | Ready now | paper skeleton; figure plan | Center workflow panel. |\n"
        "| Three-layer rubric | Ready now | CONCEPTS.md; results tables | Compact methods table. |\n"
        f"| RQ1 distribution | {_provisional_or_ready(cycle_status)} | {results_tables_md} | Results count strip. |\n"
        f"| Evidence card | {_evidence_status(evidence_candidate, cycle_status)} | {_cell(evidence_candidate)} | Site-level proof card. |\n"
        f"| Longitudinal timeline | {timeline_status} | {_cell(timeline_source)} | RQ2 change/stability panel. |\n\n"
        "## Poster Copy Blocks\n\n"
        "- Thesis: This poster presents a traceable audit workflow for scoring consent interfaces and "
        "tracking how those interfaces change over time.\n"
        f"- Methods: A focused deep sample of {target_count} sites is captured as screenshots, DOM, text, "
        "hashes, path attempts, deterministic layer scores, and longitudinal summaries.\n"
        "- Preliminary RQ1 result: banner-present automated tiers are "
        f"{_format_counts(banner_tier_counts) or 'none'}; "
        f"no-visible-banner contrast candidates={no_visible_count}; raw automated tiers are "
        f"{_format_counts(tier_counts) or 'none'}.\n"
        f"- Preliminary RQ2 result: current longitudinal severity levels are "
        f"{_format_counts(severity_counts) or 'none'}.\n"
        f"- Limitation: {poster_limitation}\n"
        "- Takeaway: the contribution is an evidence trail for interface design and drift, not a legal "
        "compliance verdict.\n\n"
        "## Before Final Poster\n\n"
        f"{before_final_poster}\n"
        "## Source Artifacts\n\n"
        f"- Targets: `{targets_csv}`\n"
        f"- RQ1 audit reports: `{audit_summary_csv}`\n"
        f"- RQ2 longitudinal summaries: `{longitudinal_summary_csv}`\n"
        f"- CMP confirmation sheet: `{cmp_confirmation_csv}`\n"
        f"- Results tables: `{results_tables_md}`\n"
        f"- Paper skeleton: `{paper_skeleton_md}`\n"
        f"- Figure plan: `{figure_plan_md}`\n"
        f"- Writing pack: `{writing_pack_md}`\n"
        f"- Claim register: `{claim_register_md}`\n"
        f"- Cycle report: `{cycle_report_md}`\n"
    )


def _poster_claim_status(cycle_status: str) -> str:
    if cycle_status in {"complete", "capture_complete", "completed", "ready", "refreshed"}:
        return "ready after sanity review."
    return "provisional until scheduled Week 2 capture is complete."


def _provisional_or_ready(cycle_status: str) -> str:
    if _poster_claim_status(cycle_status) == "ready after sanity review.":
        return "Ready after sanity review"
    return "Ready as provisional evidence"


def _timeline_status(cycle_status: str) -> str:
    if _poster_claim_status(cycle_status) == "ready after sanity review.":
        return "Ready after sanity review"
    return "Blocked for final poster by live Week 2 capture"


def _evidence_status(candidate: str, cycle_status: str) -> str:
    if candidate == "missing evidence refs":
        return "Blocked until evidence refs exist"
    if _poster_claim_status(cycle_status) == "ready after sanity review.":
        return "Ready after sanity review"
    return "Ready as provisional evidence"


def _poster_limitation(cycle_status: str) -> str:
    if _poster_claim_status(cycle_status) == "ready after sanity review.":
        return (
            "Week 2 evidence-gate claims are ready after sanity review, but the "
            "final poster still needs sample expansion and CMP/manual-review labels."
        )
    return f"final poster claims remain {_poster_claim_status(cycle_status)}"


def _before_final_poster_items(cycle_status: str) -> str:
    if _poster_claim_status(cycle_status) == "ready after sanity review.":
        items = [
            "Use the completed Week 2 gate as first evidence, not the final dataset.",
            "Resolve or explicitly label pending CMP/manual-review confirmations.",
            "Expand the deep sample toward roughly 20 sites.",
            "Render final figures from the results tables and figure plan.",
            "Re-check the claim register so poster text does not overclaim.",
        ]
    else:
        items = [
            "Run scheduled `week2-cycle` and refresh outputs.",
            "Confirm the Week 2 sanity check before freezing counts.",
            "Resolve or explicitly label pending CMP/manual-review confirmations.",
            "Render final figures from the results tables and figure plan.",
            "Re-check the claim register so poster text does not overclaim.",
        ]
    return "\n".join(f"- {item}" for item in items)


def _banner_evidence_class(report: dict[str, str]) -> str:
    if not report:
        return "missing"
    if _parse_bool(report.get("banner_detected", "")):
        return "banner_present"
    return "no_visible_banner"


def _count_banner_classes(
    targets: list[dict[str, str]],
    reports: dict[str, dict[str, str]],
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for target in targets:
        report = reports.get(_canonicalize_url(target.get("url", "")), {})
        value = _banner_evidence_class(report)
        counts[value] = counts.get(value, 0) + 1
    return counts


def _count_banner_present_values(
    targets: list[dict[str, str]],
    reports: dict[str, dict[str, str]],
    key: str,
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for target in targets:
        report = reports.get(_canonicalize_url(target.get("url", "")), {})
        if _banner_evidence_class(report) != "banner_present":
            continue
        value = (report.get(key) or "missing").strip() or "missing"
        counts[value] = counts.get(value, 0) + 1
    return counts


def _evidence_card_candidate(
    targets: list[dict[str, str]],
    reports: dict[str, dict[str, str]],
) -> str:
    candidates: list[tuple[int, str]] = []
    for index, target in enumerate(targets):
        report = _row_for(target, reports)
        screenshot = report.get("first_screenshot_ref", "")
        dom = report.get("first_dom_snapshot_ref", "")
        if not screenshot or not dom:
            continue
        tier_bonus = 0 if report.get("tier") == "Compliant" else 1
        site = target.get("name", "") or target.get("url", "")
        candidates.append((tier_bonus * 100 + index, f"{site}; {screenshot}; {dom}"))
    if not candidates:
        return "missing evidence refs"
    return min(candidates, key=lambda item: item[0])[1]


def _timeline_candidates(
    targets: list[dict[str, str]],
    summaries: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, target in enumerate(targets):
        summary = _row_for(target, summaries)
        if not summary:
            continue
        rows.append(
            {
                "site": target.get("name", "") or target.get("url", ""),
                "severity": summary.get("severity", ""),
                "event_count": summary.get("event_count", ""),
                "_index": str(index),
            }
        )
    return sorted(rows, key=_timeline_sort_key)


def _timeline_sort_key(row: dict[str, str]) -> tuple[int, int, int]:
    severity_rank = {"D": 0, "C": 1, "B": 2, "A": 3}
    return (
        severity_rank.get(row.get("severity", ""), 4),
        -_parse_int(row.get("event_count", "")),
        _parse_int(row.get("_index", "0")),
    )


def _timeline_source(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "missing longitudinal rows"
    return "; ".join(row["site"] for row in rows[:3])


def _row_for(
    target: dict[str, str],
    rows_by_url: dict[str, dict[str, str]],
) -> dict[str, str]:
    return rows_by_url.get(_canonicalize_url(target.get("url", "")), {})


def _latest_by_url(
    rows: list[dict[str, str]],
    *,
    date_key: str,
) -> dict[str, dict[str, str]]:
    latest: dict[str, dict[str, str]] = {}
    for row in rows:
        canonical_url = _canonicalize_url(row.get("url", ""))
        if not canonical_url:
            continue
        current = latest.get(canonical_url)
        if current is None or row.get(date_key, "") >= current.get(date_key, ""):
            latest[canonical_url] = row
    return latest


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as fh:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        ]


def _count_target_values(
    targets: list[dict[str, str]],
    rows_by_url: dict[str, dict[str, str]],
    key: str,
    *,
    default: str,
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for target in targets:
        row = rows_by_url.get(_canonicalize_url(target.get("url", "")), {})
        value = (row.get(key) or default).strip() or default
        counts[value] = counts.get(value, 0) + 1
    return counts


def _count_values(
    rows: list[dict[str, str]],
    key: str,
    *,
    default: str,
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = (row.get(key) or default).strip() or default
        counts[value] = counts.get(value, 0) + 1
    return counts


def _extract_capture_status(path: Path) -> str:
    if not path.exists():
        return "missing_cycle_report"
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- Capture status:"):
            return stripped.split(":", 1)[1].strip().strip("`") or "unknown"
    return "unknown"


def _format_counts(counts: dict[str, int]) -> str:
    return ", ".join(f"{key}={count}" for key, count in sorted(counts.items()))


def _parse_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def _cell(value: Path | str) -> str:
    return str(value).replace("|", "\\|")


def _canonicalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    path = parsed.path.rstrip("/")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", parsed.query, ""))
