"""Generate a paper/poster figure plan from current SSRP evidence."""

from __future__ import annotations

import csv
from pathlib import Path
from urllib.parse import urlparse, urlunparse


def export_ssrp_figure_plan(
    *,
    targets_csv: Path,
    audit_summary_csv: Path,
    longitudinal_summary_csv: Path,
    results_tables_md: Path,
    paper_skeleton_md: Path,
    cycle_report_md: Path,
    out_md: Path,
    title: str,
    week_label: str,
) -> str:
    """Write a Markdown figure plan grounded in current research artifacts."""

    targets = _read_rows(targets_csv)
    reports = _latest_by_url(_read_rows(audit_summary_csv), date_key="captured_at")
    summaries = _latest_by_url(_read_rows(longitudinal_summary_csv), date_key="week_of")
    cycle_status = _extract_capture_status(cycle_report_md)
    text = _render_figure_plan(
        title=title,
        week_label=week_label,
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        results_tables_md=results_tables_md,
        paper_skeleton_md=paper_skeleton_md,
        cycle_report_md=cycle_report_md,
        targets=targets,
        reports=reports,
        summaries=summaries,
        cycle_status=cycle_status,
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")
    return text


def _render_figure_plan(
    *,
    title: str,
    week_label: str,
    targets_csv: Path,
    audit_summary_csv: Path,
    longitudinal_summary_csv: Path,
    results_tables_md: Path,
    paper_skeleton_md: Path,
    cycle_report_md: Path,
    targets: list[dict[str, str]],
    reports: dict[str, dict[str, str]],
    summaries: dict[str, dict[str, str]],
    cycle_status: str,
) -> str:
    target_count = len(targets)
    rq1_count = sum(1 for target in targets if _row_for(target, reports))
    rq2_count = sum(1 for target in targets if _row_for(target, summaries))
    evidence_candidate = _evidence_card_candidate(targets, reports)
    timeline_candidates = _timeline_candidates(targets, summaries)
    final_timeline_status = _final_timeline_status(cycle_status)
    results_next = _results_next_action(cycle_status)
    evidence_next = _evidence_next_action(cycle_status)
    timeline_next = _timeline_next_action(cycle_status)

    return (
        f"# {title}\n\n"
        "## Evidence Snapshot\n\n"
        f"- Evidence window: {week_label}\n"
        f"- Target sites: {target_count}\n"
        f"- RQ1 figure data available: {rq1_count}/{target_count}\n"
        f"- RQ2 timeline data available: {rq2_count}/{target_count}\n"
        f"- Cycle capture status: `{cycle_status}`\n\n"
        "## Figure Readiness\n\n"
        "| Figure | Paper use | Status | Source/candidate | Next action |\n"
        "|---|---|---|---|---|\n"
        "| System architecture | Methods | Ready now | CONCEPTS.md; capture/report pipeline | Convert Mermaid draft to final figure. |\n"
        "| Three-layer rubric | Methods | Ready now | CONCEPTS.md; SCHEMA.md | Convert rubric language into a compact table. |\n"
        f"| Results distribution | RQ1 findings | {_results_status(cycle_status)} | {results_tables_md} | {results_next} |\n"
        f"| Evidence card example | Methods/Findings | {_evidence_status(evidence_candidate, cycle_status)} | {_cell(evidence_candidate)} | {evidence_next} |\n"
        f"| Longitudinal change timeline | RQ2 findings | {final_timeline_status} | {_cell(_timeline_source(timeline_candidates))} | {timeline_next} |\n"
        "| Poster workflow panel | Poster/demo | Ready now | paper skeleton; figure plan | Reuse architecture and evidence-card panels. |\n\n"
        "## Architecture Diagram Draft\n\n"
        "```mermaid\n"
        "flowchart LR\n"
        "    A[\"URL sample\"] --> B[\"Browser capture bundle\"]\n"
        "    B --> C[\"Screenshot, DOM, text, hashes\"]\n"
        "    B --> D[\"Path attempts and event log\"]\n"
        "    C --> E[\"Layer 1 path availability\"]\n"
        "    D --> F[\"Layer 2 path effort\"]\n"
        "    C --> G[\"Layer 3 text and framing\"]\n"
        "    E --> H[\"AuditReport\"]\n"
        "    F --> H\n"
        "    G --> H\n"
        "    H --> I[\"RQ1 results tables\"]\n"
        "    H --> J[\"WeeklySummary diff\"]\n"
        "    J --> K[\"RQ2 timeline\"]\n"
        "```\n\n"
        "## Timeline Candidates\n\n"
        "| Site | Category | Severity | Event count | Event types | Implication |\n"
        "|---|---|---|---|---|---|\n"
        f"{_render_timeline_rows(timeline_candidates)}\n\n"
        "## Source Artifacts\n\n"
        f"- Targets: `{targets_csv}`\n"
        f"- RQ1 audit reports: `{audit_summary_csv}`\n"
        f"- RQ2 longitudinal summaries: `{longitudinal_summary_csv}`\n"
        f"- Results tables: `{results_tables_md}`\n"
        f"- Paper skeleton: `{paper_skeleton_md}`\n"
        f"- Cycle report: `{cycle_report_md}`\n"
    )


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
        row = {
            "site": target.get("name", "") or target.get("url", ""),
            "category": target.get("category", ""),
            "severity": summary.get("severity", ""),
            "event_count": summary.get("event_count", ""),
            "event_types": _event_types(summary),
            "implication": summary.get("implications_for_user", "") or "missing",
            "_index": str(index),
        }
        rows.append(row)
    return sorted(rows, key=_timeline_sort_key)


def _timeline_sort_key(row: dict[str, str]) -> tuple[int, int, int]:
    severity_rank = {"D": 0, "C": 1, "B": 2, "A": 3}
    return (
        severity_rank.get(row.get("severity", ""), 4),
        -_parse_int(row.get("event_count", "")),
        _parse_int(row.get("_index", "0")),
    )


def _render_timeline_rows(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "| missing | missing | missing | missing | missing | Capture another observation. |"
    return "\n".join(
        "| "
        f"{_cell(row['site'])} | "
        f"{_cell(row['category'])} | "
        f"{_cell(row['severity'] or 'missing')} | "
        f"{_cell(row['event_count'] or 'missing')} | "
        f"{_cell(row['event_types'])} | "
        f"{_cell(row['implication'])} |"
        for row in rows
    )


def _final_timeline_status(cycle_status: str) -> str:
    if _is_ready_cycle(cycle_status):
        return "Ready after sanity review"
    return "Blocked for final paper by live Week 2 capture"


def _results_status(cycle_status: str) -> str:
    if _final_timeline_status(cycle_status) == "Ready after sanity review":
        return "Ready after sanity review"
    return "Ready as provisional evidence"


def _evidence_status(candidate: str, cycle_status: str) -> str:
    if candidate == "missing evidence refs":
        return "Blocked until evidence refs exist"
    if _is_ready_cycle(cycle_status):
        return "Ready after sanity review"
    return "Ready as provisional evidence"


def _results_next_action(cycle_status: str) -> str:
    if _is_ready_cycle(cycle_status):
        return "Use with current sanity check; refresh after future captures."
    return "Refresh after the scheduled capture before final claims."


def _evidence_next_action(cycle_status: str) -> str:
    if _is_ready_cycle(cycle_status):
        return "Verify selected references and build a paper evidence card."
    return "Re-capture on Week 2 and verify references before final paper."


def _timeline_next_action(cycle_status: str) -> str:
    if _is_ready_cycle(cycle_status):
        return "Choose 2-3 sites for the RQ2 timeline figure."
    return "Refresh after scheduled capture and choose 2-3 sites."


def _is_ready_cycle(cycle_status: str) -> bool:
    return cycle_status in {
        "complete",
        "ready",
        "refreshed",
        "capture_complete",
        "completed",
    }


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


def _extract_capture_status(path: Path) -> str:
    if not path.exists():
        return "missing_cycle_report"
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- Capture status:"):
            return stripped.split(":", 1)[1].strip().strip("`") or "unknown"
    return "unknown"


def _event_types(summary: dict[str, str]) -> str:
    event_types = summary.get("event_types", "")
    return event_types.replace("|", "+") if event_types else "none"


def _parse_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def _cell(value: Path | str) -> str:
    return str(value).replace("|", "\\|")


def _canonicalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    path = parsed.path.rstrip("/")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", parsed.query, ""))
