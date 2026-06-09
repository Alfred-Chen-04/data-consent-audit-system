"""Generate a paper writing pack grounded in current SSRP evidence."""

from __future__ import annotations

import csv
from pathlib import Path
from urllib.parse import urlparse, urlunparse


def export_ssrp_writing_pack(
    *,
    targets_csv: Path,
    audit_summary_csv: Path,
    longitudinal_summary_csv: Path,
    cmp_confirmation_csv: Path,
    results_tables_md: Path,
    paper_skeleton_md: Path,
    figure_plan_md: Path,
    cycle_report_md: Path,
    out_md: Path,
    title: str,
    week_label: str,
) -> str:
    """Write a Markdown drafting pack for methods/results/discussion sections."""

    targets = _read_rows(targets_csv)
    reports = _latest_by_url(_read_rows(audit_summary_csv), date_key="captured_at")
    summaries = _latest_by_url(_read_rows(longitudinal_summary_csv), date_key="week_of")
    confirmation_counts = _count_values(
        _read_rows(cmp_confirmation_csv),
        "confirmation_status",
        default="pending",
    )
    cycle_status = _extract_capture_status(cycle_report_md)
    text = _render_writing_pack(
        title=title,
        week_label=week_label,
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        cmp_confirmation_csv=cmp_confirmation_csv,
        results_tables_md=results_tables_md,
        paper_skeleton_md=paper_skeleton_md,
        figure_plan_md=figure_plan_md,
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


def _render_writing_pack(
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
    cycle_report_md: Path,
    targets: list[dict[str, str]],
    reports: dict[str, dict[str, str]],
    summaries: dict[str, dict[str, str]],
    confirmation_counts: dict[str, int],
    cycle_status: str,
) -> str:
    target_count = len(targets)
    report_count = sum(1 for target in targets if _row_for(target, reports))
    summary_count = sum(1 for target in targets if _row_for(target, summaries))
    tier_counts = _count_target_values(targets, reports, "tier", default="missing")
    banner_counts = _count_banner_classes(targets, reports)
    banner_tier_counts = _count_banner_present_values(targets, reports, "tier")
    no_visible_count = banner_counts.get("no_visible_banner", 0)
    severity_counts = _count_target_values(targets, summaries, "severity", default="missing")
    category_counts = _count_values(targets, "category", default="unknown")
    claim_status = _claim_status(cycle_status)
    cmp_status = _format_counts(confirmation_counts) or "none"
    capture_limitation = _capture_limitation(cycle_status)
    drafting_gate = _drafting_gate(cycle_status)

    return (
        f"# {title}\n\n"
        "## Evidence Snapshot\n\n"
        f"- Evidence window: {week_label}\n"
        f"- Target sites: {target_count}\n"
        f"- Categories: {_format_counts(category_counts) or 'none'}\n"
        f"- RQ1 reports available for targets: {report_count}/{target_count}\n"
        f"- RQ2 summaries available for targets: {summary_count}/{target_count}\n"
        f"- Banner evidence classes: {_format_counts(banner_counts) or 'none'}\n"
        f"- Banner-present automated tiers: {_format_counts(banner_tier_counts) or 'none'}\n"
        f"- Raw automated target tiers: {_format_counts(tier_counts) or 'none'}\n"
        f"- Latest longitudinal severity: {_format_counts(severity_counts) or 'none'}\n"
        f"- CMP confirmations: {cmp_status}\n"
        f"- Cycle capture status: `{cycle_status}`\n"
        f"- Claim status: {claim_status}\n\n"
        "## Methods Draft Blocks\n\n"
        f"- Sample: This pilot uses a focused deep sample of {target_count} public websites "
        "selected for repeated evidence capture rather than a broad one-time crawl.\n"
        "- Capture unit: each observation stores a screenshot, DOM snapshot, visible text, "
        "path-attempt log, hashes, and report references so later claims can be traced back "
        "to concrete evidence.\n"
        "- Scoring discipline: model extraction can assist with text or visual cues, but final "
        "grades are produced by deterministic scoring after schema validation and evidence checks.\n"
        "- Longitudinal unit: weekly summaries compare path availability, scores, text, DOM, "
        "layout, and fingerprint evidence so RQ2 can separate stable interfaces from changed ones.\n\n"
        "## Preliminary Results Notes\n\n"
        f"- RQ1: banner-present automated tiers are {_format_counts(banner_tier_counts) or 'none'}.\n"
        f"- RQ1 contrast context: no-visible-banner contrast candidates={no_visible_count}; "
        f"raw automated tiers are {_format_counts(tier_counts) or 'none'}.\n"
        f"- RQ2: latest target longitudinal severity levels are {_format_counts(severity_counts) or 'none'}.\n"
        f"- Current claims remain {claim_status}\n"
        f"- Highest-priority longitudinal candidates: {_top_longitudinal_sites(targets, summaries)}.\n"
        f"- RQ1 result source: `{results_tables_md}`.\n\n"
        "## Discussion And Implication Notes\n\n"
        "- The strongest contribution is the traceable link from visible consent-interface design "
        "to longitudinal evidence, not a legal conclusion about compliance.\n"
        "- Use the longitudinal rows to explain why a single screenshot audit can miss meaningful "
        "interface drift, especially copy, layout, DOM, and pathway changes.\n"
        "- Keep the small GRC/SOC 2 implication bounded: consent-interface evidence may support "
        "privacy readiness conversations, but this project is not a SOC 2 audit system.\n\n"
        "## Limitations To Carry Forward\n\n"
        "- Desktop public-page capture only; authenticated, mobile, geolocated, and user-history "
        "specific experiences may differ.\n"
        "- English-focused visible text extraction and deterministic fallbacks may miss localized "
        "or heavily visual consent cues.\n"
        f"- {capture_limitation}\n"
        f"- pending CMP/manual-review confirmations remain unresolved: {cmp_status}.\n"
        "- Scores describe interface evidence, not legal compliance or user intent.\n\n"
        "## Drafting Checklist\n\n"
        f"- {drafting_gate}\n"
        "- Run `consent-audit ssrp-claim-register` before polishing results prose.\n"
        "- Re-run `week2-refresh-outputs` after live capture before copying tables or figure notes.\n"
        "- Use exact screenshot, DOM, hash, and quote evidence when writing any site-specific claim.\n"
        "- Keep SOC 2/GRC framing to a brief implication paragraph.\n\n"
        "## Source Artifacts\n\n"
        f"- Targets: `{targets_csv}`\n"
        f"- RQ1 audit reports: `{audit_summary_csv}`\n"
        f"- RQ2 longitudinal summaries: `{longitudinal_summary_csv}`\n"
        f"- CMP confirmation sheet: `{cmp_confirmation_csv}`\n"
        f"- Results tables: `{results_tables_md}`\n"
        f"- Paper skeleton: `{paper_skeleton_md}`\n"
        f"- Figure plan: `{figure_plan_md}`\n"
        f"- Cycle report: `{cycle_report_md}`\n"
    )


def _claim_status(cycle_status: str) -> str:
    if _is_ready_cycle(cycle_status):
        return "ready for post-sanity drafting."
    return "provisional until scheduled Week 2 capture is complete."


def _capture_limitation(cycle_status: str) -> str:
    if _is_ready_cycle(cycle_status):
        return (
            f"Scheduled Week 2 live capture status is `{cycle_status}`; result "
            "claims should cite the sanity check and source evidence references."
        )
    return (
        f"Scheduled Week 2 live capture status is `{cycle_status}`, so final "
        "results should wait for fresh capture and sanity confirmation."
    )


def _drafting_gate(cycle_status: str) -> str:
    if _is_ready_cycle(cycle_status):
        return (
            "Use ready Week 2 result claims only with the sanity check and "
            "source evidence refs."
        )
    return "Do not turn provisional results into final claims until `week2-cycle` completes."


def _is_ready_cycle(cycle_status: str) -> bool:
    return cycle_status in {"complete", "capture_complete", "completed", "ready", "refreshed"}


def _top_longitudinal_sites(
    targets: list[dict[str, str]],
    summaries: dict[str, dict[str, str]],
) -> str:
    candidates: list[tuple[int, int, int, str]] = []
    severity_rank = {"D": 0, "C": 1, "B": 2, "A": 3}
    for index, target in enumerate(targets):
        summary = _row_for(target, summaries)
        if not summary:
            continue
        site = target.get("name", "") or target.get("url", "")
        candidates.append(
            (
                severity_rank.get(summary.get("severity", ""), 4),
                -_parse_int(summary.get("event_count", "")),
                index,
                site,
            )
        )
    if not candidates:
        return "none yet"
    return ", ".join(row[3] for row in sorted(candidates)[:3])


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


def _canonicalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    path = parsed.path.rstrip("/")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", parsed.query, ""))
