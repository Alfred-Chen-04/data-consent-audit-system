"""Week 2 capture sanity checks over research export tables."""

from __future__ import annotations

import csv
from pathlib import Path
from urllib.parse import urlparse, urlunparse

EVIDENCE_FIELDS = (
    "first_screenshot_ref",
    "first_dom_snapshot_ref",
    "dom_hash",
    "image_hash",
)


def export_week2_sanity_check(
    *,
    targets_csv: Path,
    consent_table_csv: Path,
    audit_summary_csv: Path,
    longitudinal_summary_csv: Path,
    out_md: Path,
    cohort: str,
    week_of: str,
    title: str,
) -> str:
    """Write a Markdown check of whether Week 2 target evidence is complete."""

    targets = _read_rows(targets_csv)
    consent_by_url = _latest_consent_rows_for_cohort(
        _read_rows(consent_table_csv),
        cohort=cohort,
    )
    reports_by_url = _reports_by_url(_read_rows(audit_summary_csv))
    summaries_by_url = _summaries_by_url(
        _read_rows(longitudinal_summary_csv),
        week_of=week_of,
    )

    checks = [
        _check_target(
            target,
            consent_by_url=consent_by_url,
            reports_by_url=reports_by_url,
            summaries_by_url=summaries_by_url,
            cohort=cohort,
        )
        for target in targets
    ]
    text = _render_sanity_check(
        title=title,
        cohort=cohort,
        week_of=week_of,
        checks=checks,
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")
    return text


def _check_target(
    target: dict[str, str],
    *,
    consent_by_url: dict[str, dict[str, str]],
    reports_by_url: dict[str, list[dict[str, str]]],
    summaries_by_url: dict[str, list[dict[str, str]]],
    cohort: str,
) -> dict[str, str]:
    canonical_url = _canonicalize_url(target.get("url", ""))
    consent = consent_by_url.get(canonical_url)
    if consent is None:
        return {
            "name": target.get("name", "") or target.get("url", ""),
            "category": target.get("category", ""),
            "consent": "missing",
            "evidence": "not checked",
            "report": "missing",
            "summary": "missing",
            "notes": f"No consent-table row for cohort {cohort}",
        }

    evidence_complete = all((consent.get(field) or "").strip() for field in EVIDENCE_FIELDS)
    report_matched = _has_matching_report(consent, reports_by_url.get(canonical_url, []))
    summary_present = bool(summaries_by_url.get(canonical_url))
    notes: list[str] = []
    if not evidence_complete:
        notes.append("Consent row missing screenshot/DOM/hash evidence.")
    if not report_matched:
        notes.append("No audit report matches consent row fingerprints.")
    if not summary_present:
        notes.append("No weekly summary found for the expected week.")

    return {
        "name": target.get("name", "") or target.get("url", ""),
        "category": target.get("category", ""),
        "consent": "captured",
        "evidence": "complete" if evidence_complete else "incomplete",
        "report": "matched" if report_matched else "missing",
        "summary": "present" if summary_present else "missing",
        "notes": " ".join(notes) if notes else "Ready for advisor review.",
    }


def _render_sanity_check(
    *,
    title: str,
    cohort: str,
    week_of: str,
    checks: list[dict[str, str]],
) -> str:
    target_count = len(checks)
    captured_count = _count_status(checks, "consent", "captured")
    evidence_count = _count_status(checks, "evidence", "complete")
    report_count = _count_status(checks, "report", "matched")
    summary_count = _count_status(checks, "summary", "present")
    status = _overall_status(
        target_count=target_count,
        captured_count=captured_count,
        evidence_count=evidence_count,
        report_count=report_count,
    )
    table_rows = "\n".join(_render_check_row(check) for check in checks)

    return (
        f"# {title}\n\n"
        "## Summary\n\n"
        f"- Cohort: `{cohort}`\n"
        f"- Expected week: `{week_of}`\n"
        f"- Target sites: {target_count}\n"
        f"- Consent rows captured: {captured_count}/{target_count}\n"
        f"- Evidence-complete rows: {evidence_count}/{target_count}\n"
        f"- Matching audit reports: {report_count}/{target_count}\n"
        f"- Weekly summaries present: {summary_count}/{target_count}\n"
        f"- Overall status: {status}\n\n"
        "## Site Checks\n\n"
        "| Site | Consent row | Evidence | Audit report | Weekly summary | Notes |\n"
        "|---|---|---|---|---|---|\n"
        f"{table_rows}\n"
    )


def _render_check_row(check: dict[str, str]) -> str:
    return (
        "| "
        f"{_escape_table_cell(check.get('name', ''))} | "
        f"{check.get('consent', '')} | "
        f"{check.get('evidence', '')} | "
        f"{check.get('report', '')} | "
        f"{check.get('summary', '')} | "
        f"{_escape_table_cell(check.get('notes', ''))} |"
    )


def _overall_status(
    *,
    target_count: int,
    captured_count: int,
    evidence_count: int,
    report_count: int,
) -> str:
    if target_count == 0 or captured_count == 0:
        return "pending_capture"
    if (
        captured_count < target_count
        or evidence_count < target_count
        or report_count < target_count
    ):
        return "needs_attention"
    return "ready"


def _latest_consent_rows_for_cohort(
    rows: list[dict[str, str]],
    *,
    cohort: str,
) -> dict[str, dict[str, str]]:
    latest: dict[str, dict[str, str]] = {}
    for row in rows:
        if row.get("cohort", "") != cohort:
            continue
        canonical_url = _canonicalize_url(row.get("url", ""))
        if not canonical_url:
            continue
        current = latest.get(canonical_url)
        if current is None or row.get("captured_at", "") > current.get("captured_at", ""):
            latest[canonical_url] = row
    return latest


def _reports_by_url(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    reports: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        canonical_url = _canonicalize_url(row.get("url", ""))
        if canonical_url:
            reports.setdefault(canonical_url, []).append(row)
    return reports


def _summaries_by_url(
    rows: list[dict[str, str]],
    *,
    week_of: str,
) -> dict[str, list[dict[str, str]]]:
    summaries: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        if row.get("week_of", "") < week_of:
            continue
        canonical_url = _canonicalize_url(row.get("url", ""))
        if canonical_url:
            summaries.setdefault(canonical_url, []).append(row)
    return summaries


def _has_matching_report(
    consent: dict[str, str],
    reports: list[dict[str, str]],
) -> bool:
    dom_hash = consent.get("dom_hash", "")
    image_hash = consent.get("image_hash", "")
    for report in reports:
        if dom_hash and report.get("dom_hash", "") == dom_hash:
            return True
        if image_hash and report.get("image_hash", "") == image_hash:
            return True
    return False


def _count_status(checks: list[dict[str, str]], key: str, expected: str) -> int:
    return sum(1 for check in checks if check.get(key) == expected)


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as fh:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        ]


def _escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|")


def _canonicalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    path = parsed.path.rstrip("/")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", parsed.query, ""))
