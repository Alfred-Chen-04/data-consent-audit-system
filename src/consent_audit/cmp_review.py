"""Build CMP/manual review queues from sample readiness evidence."""

from __future__ import annotations

import csv
import os
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from html import escape
from pathlib import Path
from re import sub
from urllib.parse import urlparse, urlunparse


@dataclass(frozen=True)
class CmpReviewQueueRow:
    url: str
    name: str
    category: str
    cohort: str
    readiness_status: str
    readiness_notes: str
    access_banner_detected: bool
    consent_banner_detected: bool
    capture_observed: bool
    capture_date: str
    tier: str
    access_screenshot_path: str
    capture_screenshot_ref: str
    capture_dom_snapshot_ref: str
    dom_hash: str
    image_hash: str
    review_reason: str
    recommended_action: str


@dataclass(frozen=True)
class CmpReviewWorksheetRow:
    url: str
    name: str
    category: str
    cohort: str
    readiness_status: str
    access_screenshot_path: str
    capture_screenshot_ref: str
    capture_dom_snapshot_ref: str
    review_reason: str
    recommended_action: str
    review_question: str
    decision_options: str
    manual_banner_observed: str
    manual_cmp_vendor: str
    sample_decision: str
    reviewer: str
    reviewed_at: str
    reviewer_notes: str


@dataclass(frozen=True)
class CmpReviewSuggestionRow:
    url: str
    name: str
    category: str
    cohort: str
    readiness_status: str
    capture_dom_snapshot_ref: str
    auto_suggested_decision: str
    confidence: str
    evidence_summary: str
    dom_indicator_terms: str
    requires_human_confirmation: bool


@dataclass(frozen=True)
class CmpReviewDecisionDraftRow:
    url: str
    name: str
    category: str
    cohort: str
    draft_decision: str
    draft_confidence: str
    source_auto_suggestion: str
    draft_rationale: str
    recommended_next_step: str
    requires_human_confirmation: bool


@dataclass(frozen=True)
class CmpReviewConfirmationRow:
    url: str
    name: str
    category: str
    cohort: str
    draft_decision: str
    draft_confidence: str
    source_auto_suggestion: str
    draft_rationale: str
    recommended_next_step: str
    confirmation_status: str
    confirmed_decision: str
    manual_banner_observed: str
    manual_cmp_vendor: str
    reviewer: str
    reviewed_at: str
    reviewer_notes: str


FIELDNAMES = list(CmpReviewQueueRow.__dataclass_fields__.keys())
WORKSHEET_FIELDNAMES = list(CmpReviewWorksheetRow.__dataclass_fields__.keys())
SUGGESTION_FIELDNAMES = list(CmpReviewSuggestionRow.__dataclass_fields__.keys())
DECISION_DRAFT_FIELDNAMES = list(CmpReviewDecisionDraftRow.__dataclass_fields__.keys())
CONFIRMATION_FIELDNAMES = list(CmpReviewConfirmationRow.__dataclass_fields__.keys())
RERUN_TARGET_FIELDNAMES = [
    "url",
    "name",
    "category",
    "inherited_from_phd_mentor",
    "notes",
]

NO_BANNER_REVIEW_REASON = (
    "no banner observed in access probe or weekly capture; inspect saved "
    "screenshots/DOM to verify CMP presence, region behavior, or sample fit"
)
DEFAULT_RECOMMENDED_ACTION = (
    "manual screenshot/DOM review; rerun with fresh browser context if a CMP is expected"
)
REVIEW_QUESTION = (
    "Inspect the access and capture evidence; decide whether this is a true "
    "no-banner case, a missed CMP, or a candidate to rerun/replace."
)
DECISION_OPTIONS = (
    "keep_consent_sample|keep_no_banner_case|rerun_fresh_context|"
    "replace_candidate|exclude"
)
ALLOWED_DECISIONS = set(DECISION_OPTIONS.split("|"))
DOM_INDICATOR_TERMS = (
    "onetrust",
    "cookiebot",
    "usercentrics",
    "sourcepoint",
    "trustarc",
    "didomi",
    "quantcast",
    "cookie",
    "consent",
    "gdpr",
    "ccpa",
    "privacy choices",
    "do not sell",
    "preference center",
)


def build_cmp_review_queue(
    readiness_csv: Path,
    consent_table_csv: Path | Sequence[Path],
) -> list[CmpReviewQueueRow]:
    """Return readiness rows that need manual CMP review, enriched with evidence refs."""
    consent_rows = _read_latest_by_url(consent_table_csv)
    rows: list[CmpReviewQueueRow] = []

    with readiness_csv.open(encoding="utf-8") as fh:
        for readiness in csv.DictReader(fh):
            status = (readiness.get("readiness_status") or "").strip()
            if status != "needs_cmp_review":
                continue

            url = (readiness.get("url") or "").strip()
            consent = consent_rows.get(_canonicalize_url(url), {})
            access_banner_detected = _parse_bool(readiness.get("access_banner_detected"))
            consent_banner_detected = _parse_bool(
                readiness.get("consent_banner_detected")
            )

            rows.append(
                CmpReviewQueueRow(
                    url=url,
                    name=(readiness.get("name") or "").strip(),
                    category=(readiness.get("category") or "").strip(),
                    cohort=(readiness.get("cohort") or "").strip(),
                    readiness_status=status,
                    readiness_notes=(readiness.get("readiness_notes") or "").strip(),
                    access_banner_detected=access_banner_detected,
                    consent_banner_detected=consent_banner_detected,
                    capture_observed=_parse_bool(readiness.get("capture_observed")),
                    capture_date=(
                        consent.get("capture_date")
                        or readiness.get("capture_date")
                        or ""
                    ).strip(),
                    tier=(consent.get("tier") or readiness.get("tier") or "").strip(),
                    access_screenshot_path=(
                        readiness.get("access_screenshot_path") or ""
                    ).strip(),
                    capture_screenshot_ref=(
                        consent.get("first_screenshot_ref") or ""
                    ).strip(),
                    capture_dom_snapshot_ref=(
                        consent.get("first_dom_snapshot_ref") or ""
                    ).strip(),
                    dom_hash=(consent.get("dom_hash") or "").strip(),
                    image_hash=(consent.get("image_hash") or "").strip(),
                    review_reason=_review_reason(
                        access_banner_detected=access_banner_detected,
                        consent_banner_detected=consent_banner_detected,
                    ),
                    recommended_action=DEFAULT_RECOMMENDED_ACTION,
                )
            )

    return rows


def export_cmp_review_queue_to_csv(
    out_csv: Path,
    rows: list[CmpReviewQueueRow],
) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            record = asdict(row)
            record["access_banner_detected"] = _format_bool(row.access_banner_detected)
            record["consent_banner_detected"] = _format_bool(row.consent_banner_detected)
            record["capture_observed"] = _format_bool(row.capture_observed)
            writer.writerow(record)


def summarize_cmp_review_queue(rows: list[CmpReviewQueueRow]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for row in rows:
        summary[row.readiness_status] = summary.get(row.readiness_status, 0) + 1
    return summary


def build_cmp_review_worksheet(queue_csv: Path) -> list[CmpReviewWorksheetRow]:
    """Create a fillable manual decision worksheet from the CMP review queue."""
    rows: list[CmpReviewWorksheetRow] = []
    with queue_csv.open(encoding="utf-8") as fh:
        for queue_row in csv.DictReader(fh):
            url = (queue_row.get("url") or "").strip()
            if not url:
                continue
            rows.append(
                CmpReviewWorksheetRow(
                    url=url,
                    name=(queue_row.get("name") or "").strip(),
                    category=(queue_row.get("category") or "").strip(),
                    cohort=(queue_row.get("cohort") or "").strip(),
                    readiness_status=(queue_row.get("readiness_status") or "").strip(),
                    access_screenshot_path=(
                        queue_row.get("access_screenshot_path") or ""
                    ).strip(),
                    capture_screenshot_ref=(
                        queue_row.get("capture_screenshot_ref") or ""
                    ).strip(),
                    capture_dom_snapshot_ref=(
                        queue_row.get("capture_dom_snapshot_ref") or ""
                    ).strip(),
                    review_reason=(queue_row.get("review_reason") or "").strip(),
                    recommended_action=(
                        queue_row.get("recommended_action") or ""
                    ).strip(),
                    review_question=REVIEW_QUESTION,
                    decision_options=DECISION_OPTIONS,
                    manual_banner_observed="",
                    manual_cmp_vendor="",
                    sample_decision="",
                    reviewer="",
                    reviewed_at="",
                    reviewer_notes="",
                )
            )
    return rows


def export_cmp_review_worksheet_to_csv(
    out_csv: Path,
    rows: list[CmpReviewWorksheetRow],
) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=WORKSHEET_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def export_cmp_review_packet(
    queue_csv: Path,
    out_dir: Path,
    *,
    project_root: Path = Path("."),
) -> dict[str, str | int]:
    """Write a static visual review packet for pending CMP/manual decisions."""

    rows = _read_queue_rows(queue_csv)
    out_dir.mkdir(parents=True, exist_ok=True)
    index_html = out_dir / "index.html"
    index_markdown = out_dir / "index.md"
    index_html.write_text(
        _render_packet_html(rows, out_dir=out_dir, project_root=project_root),
        encoding="utf-8",
    )
    index_markdown.write_text(
        _render_packet_markdown(rows, out_dir=out_dir, project_root=project_root),
        encoding="utf-8",
    )
    return {
        "row_count": len(rows),
        "index_html": str(index_html),
        "index_markdown": str(index_markdown),
    }


def build_cmp_review_suggestions(
    queue_csv: Path,
    *,
    project_root: Path = Path("."),
) -> list[CmpReviewSuggestionRow]:
    """Return non-final decision suggestions from queue metadata and DOM indicators."""

    rows: list[CmpReviewSuggestionRow] = []
    for queue_row in _read_queue_rows(queue_csv):
        indicator_terms, dom_status = _read_dom_indicator_terms(
            queue_row.get("capture_dom_snapshot_ref", ""),
            project_root=project_root,
        )
        decision, confidence, evidence_summary = _suggest_cmp_review_decision(
            queue_row,
            indicator_terms=indicator_terms,
            dom_status=dom_status,
        )
        rows.append(
            CmpReviewSuggestionRow(
                url=queue_row.get("url", ""),
                name=queue_row.get("name", ""),
                category=queue_row.get("category", ""),
                cohort=queue_row.get("cohort", ""),
                readiness_status=queue_row.get("readiness_status", ""),
                capture_dom_snapshot_ref=queue_row.get("capture_dom_snapshot_ref", ""),
                auto_suggested_decision=decision,
                confidence=confidence,
                evidence_summary=evidence_summary,
                dom_indicator_terms="|".join(indicator_terms),
                requires_human_confirmation=True,
            )
        )
    return rows


def export_cmp_review_suggestions_to_csv(
    out_csv: Path,
    rows: list[CmpReviewSuggestionRow],
) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=SUGGESTION_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            record = asdict(row)
            record["requires_human_confirmation"] = _format_bool(
                row.requires_human_confirmation
            )
            writer.writerow(record)


def export_cmp_review_rerun_targets(
    suggestions_csv: Path,
    out_csv: Path,
) -> int:
    """Write a weekly site-list CSV for suggestions that need fresh-context reruns."""

    rows = _read_suggestion_rows(suggestions_csv)
    target_rows = _deduplicate_rerun_targets(
        [
            row
            for row in rows
            if (row.get("auto_suggested_decision") or "").strip()
            == "rerun_fresh_context"
        ]
    )
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=RERUN_TARGET_FIELDNAMES)
        writer.writeheader()
        for row in target_rows:
            writer.writerow(
                {
                    "url": row["url"],
                    "name": row["name"],
                    "category": row["category"],
                    "inherited_from_phd_mentor": "false",
                    "notes": _rerun_target_notes(row),
                }
            )
    return len(target_rows)


def build_cmp_review_decision_draft(
    queue_csv: Path,
    suggestions_csv: Path,
) -> list[CmpReviewDecisionDraftRow]:
    """Create non-final worksheet decision drafts for advisor review."""
    suggestions = {
        _canonicalize_url(row.get("url", "")): row
        for row in _read_suggestion_rows(suggestions_csv)
    }
    rows: list[CmpReviewDecisionDraftRow] = []
    for queue_row in _read_queue_rows(queue_csv):
        url = queue_row.get("url", "")
        suggestion = suggestions.get(_canonicalize_url(url), {})
        decision, confidence, rationale, next_step = _draft_manual_decision(
            queue_row,
            suggestion,
        )
        rows.append(
            CmpReviewDecisionDraftRow(
                url=url,
                name=queue_row.get("name", ""),
                category=queue_row.get("category", ""),
                cohort=queue_row.get("cohort", ""),
                draft_decision=decision,
                draft_confidence=confidence,
                source_auto_suggestion=suggestion.get("auto_suggested_decision", ""),
                draft_rationale=rationale,
                recommended_next_step=next_step,
                requires_human_confirmation=True,
            )
        )
    return rows


def export_cmp_review_decision_draft_to_csv(
    out_csv: Path,
    rows: list[CmpReviewDecisionDraftRow],
) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=DECISION_DRAFT_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            record = asdict(row)
            record["requires_human_confirmation"] = _format_bool(
                row.requires_human_confirmation
            )
            writer.writerow(record)


def summarize_cmp_review_decision_draft(
    rows: list[CmpReviewDecisionDraftRow],
) -> dict[str, int]:
    summary: dict[str, int] = {}
    for row in rows:
        summary[row.draft_decision] = summary.get(row.draft_decision, 0) + 1
    return summary


def build_cmp_review_confirmation_sheet(
    draft_csv: Path,
) -> list[CmpReviewConfirmationRow]:
    """Create a human-fillable confirmation sheet from non-final draft decisions."""

    rows: list[CmpReviewConfirmationRow] = []
    for draft in _read_decision_draft_rows(draft_csv):
        rows.append(
            CmpReviewConfirmationRow(
                url=draft.get("url", ""),
                name=draft.get("name", ""),
                category=draft.get("category", ""),
                cohort=draft.get("cohort", ""),
                draft_decision=draft.get("draft_decision", ""),
                draft_confidence=draft.get("draft_confidence", ""),
                source_auto_suggestion=draft.get("source_auto_suggestion", ""),
                draft_rationale=draft.get("draft_rationale", ""),
                recommended_next_step=draft.get("recommended_next_step", ""),
                confirmation_status="pending",
                confirmed_decision="",
                manual_banner_observed="",
                manual_cmp_vendor="",
                reviewer="",
                reviewed_at="",
                reviewer_notes="",
            )
        )
    return rows


def export_cmp_review_confirmation_sheet_to_csv(
    out_csv: Path,
    rows: list[CmpReviewConfirmationRow],
) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CONFIRMATION_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def summarize_cmp_review_confirmation_sheet(
    rows: list[CmpReviewConfirmationRow],
) -> dict[str, int]:
    summary: dict[str, int] = {}
    for row in rows:
        status = row.confirmation_status or "pending"
        summary[status] = summary.get(status, 0) + 1
    return summary


def apply_cmp_review_confirmations_to_worksheet(
    worksheet_csv: Path,
    confirmation_csv: Path,
    out_csv: Path,
) -> dict[str, int]:
    """Write a worksheet copy with only explicitly confirmed decisions applied."""

    worksheet_rows, worksheet_fieldnames = _read_csv_rows_with_fieldnames(worksheet_csv)
    worksheet_urls = {
        _canonicalize_url(row.get("url", ""))
        for row in worksheet_rows
        if (row.get("url") or "").strip()
    }
    updates: dict[str, dict[str, str]] = {}
    summary: dict[str, int] = {}

    for confirmation in _read_confirmation_rows(confirmation_csv):
        canonical_url = _canonicalize_url(confirmation.get("url", ""))
        status = (confirmation.get("confirmation_status") or "pending").strip().lower()
        if status != "confirmed":
            _increment(summary, status or "pending")
            continue

        decision = (confirmation.get("confirmed_decision") or "").strip()
        if decision not in ALLOWED_DECISIONS:
            _increment(summary, "invalid_decision")
            continue
        if canonical_url not in worksheet_urls:
            _increment(summary, "unknown_url")
            continue

        updates[canonical_url] = confirmation
        _increment(summary, "applied")

    for row in worksheet_rows:
        update = updates.get(_canonicalize_url(row.get("url", "")))
        if not update:
            continue
        row["manual_banner_observed"] = update.get("manual_banner_observed", "")
        row["manual_cmp_vendor"] = update.get("manual_cmp_vendor", "")
        row["sample_decision"] = update.get("confirmed_decision", "")
        row["reviewer"] = update.get("reviewer", "")
        row["reviewed_at"] = update.get("reviewed_at", "")
        row["reviewer_notes"] = update.get("reviewer_notes", "")

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = worksheet_fieldnames or WORKSHEET_FIELDNAMES
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(worksheet_rows)

    return summary


def summarize_cmp_review_suggestions(
    rows: list[CmpReviewSuggestionRow],
) -> dict[str, int]:
    summary: dict[str, int] = {}
    for row in rows:
        decision = row.auto_suggested_decision
        summary[decision] = summary.get(decision, 0) + 1
    return summary


def summarize_cmp_review_worksheet(
    rows: list[CmpReviewWorksheetRow],
) -> dict[str, int]:
    summary: dict[str, int] = {}
    for row in rows:
        decision = row.sample_decision or "pending_manual_decision"
        summary[decision] = summary.get(decision, 0) + 1
    return summary


def _read_queue_rows(queue_csv: Path) -> list[dict[str, str]]:
    with queue_csv.open(encoding="utf-8") as fh:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        ]


def _read_suggestion_rows(suggestions_csv: Path) -> list[dict[str, str]]:
    with suggestions_csv.open(encoding="utf-8") as fh:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        ]


def _read_decision_draft_rows(draft_csv: Path) -> list[dict[str, str]]:
    with draft_csv.open(encoding="utf-8") as fh:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        ]


def _read_confirmation_rows(confirmation_csv: Path) -> list[dict[str, str]]:
    with confirmation_csv.open(encoding="utf-8") as fh:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        ]


def _read_csv_rows_with_fieldnames(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
            if (row.get("url") or "").strip()
        ]
    return rows, fieldnames


def _increment(summary: dict[str, int], key: str) -> None:
    summary[key] = summary.get(key, 0) + 1


def _deduplicate_rerun_targets(rows: list[dict[str, str]]) -> list[dict[str, str]]:
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
                "url": url,
                "name": (row.get("name") or "").strip(),
                "category": (row.get("category") or "").strip(),
                "confidence": (row.get("confidence") or "").strip(),
                "dom_indicator_terms": (row.get("dom_indicator_terms") or "").strip(),
            }
        )
    return targets


def _rerun_target_notes(row: dict[str, str]) -> str:
    return (
        "cmp_review_suggestion: rerun_fresh_context; "
        f"confidence={row.get('confidence', '')}; "
        f"indicators={row.get('dom_indicator_terms', '')}"
    )


def _draft_manual_decision(
    queue_row: dict[str, str],
    suggestion: dict[str, str],
) -> tuple[str, str, str, str]:
    host = urlparse(queue_row.get("url", "")).netloc.lower()
    if host in {"www.reddit.com", "reddit.com", "www.walmart.com", "walmart.com"}:
        return (
            "replace_candidate",
            "medium",
            "Draft based on manual-review brief: current evidence looks like access-friction rather than a clean consent-interface or no-banner observation.",
            "confirm in packet/contact sheet; replace unless advisor wants an access-friction canary",
        )

    return (
        "keep_no_banner_case",
        "low",
        "Draft based on repeated no-banner evidence: possible no-banner contrast case, not a banner-present consent sample.",
        "human reviewer should confirm screenshot/DOM evidence and decide whether no-banner contrast rows fit the methods",
    )


def _read_dom_indicator_terms(
    dom_ref: str,
    *,
    project_root: Path,
) -> tuple[list[str], str]:
    if not dom_ref.strip():
        return [], "missing_dom_ref"
    dom_path = _resolve_local_ref(dom_ref, project_root=project_root)
    if not dom_path.exists():
        return [], "missing_dom_file"
    dom_text = dom_path.read_text(encoding="utf-8", errors="ignore").lower()
    terms = [term for term in DOM_INDICATOR_TERMS if term in dom_text]
    return terms, "dom_read"


def _suggest_cmp_review_decision(
    queue_row: dict[str, str],
    *,
    indicator_terms: list[str],
    dom_status: str,
) -> tuple[str, str, str]:
    if _parse_bool(queue_row.get("access_banner_detected")) or _parse_bool(
        queue_row.get("consent_banner_detected")
    ):
        return (
            "keep_consent_sample",
            "high",
            "At least one capture source observed a banner; confirm in the packet before locking.",
        )

    if not _parse_bool(queue_row.get("capture_observed")):
        return (
            "rerun_fresh_context",
            "high",
            "No weekly capture evidence is available; rerun before making a sample decision.",
        )

    if dom_status != "dom_read":
        return (
            "rerun_fresh_context",
            "medium",
            f"DOM evidence is unavailable ({dom_status}); rerun or inspect manually.",
        )

    if indicator_terms:
        return (
            "rerun_fresh_context",
            "medium",
            "DOM contains CMP/consent indicators but no banner was observed; rerun with a fresh context or inspect the packet.",
        )

    return (
        "keep_no_banner_case",
        "low",
        "No banner was observed and the captured DOM lacks configured CMP indicators; keep only if a no-banner contrast case is useful.",
    )


def _resolve_local_ref(ref: str, *, project_root: Path) -> Path:
    path = Path(ref.strip())
    if path.is_absolute():
        return path
    candidate = project_root / path
    if candidate.exists() or path.parts[:1] != ("captures",):
        return candidate
    return project_root / "data" / path


def _render_packet_html(
    rows: list[dict[str, str]],
    *,
    out_dir: Path,
    project_root: Path,
) -> str:
    cards = "\n".join(
        _render_packet_html_card(row, out_dir=out_dir, project_root=project_root)
        for row in rows
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CMP Manual Review Packet</title>
  <style>
    :root {{
      color-scheme: light;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #f6f7f9;
      color: #172033;
    }}
    body {{
      margin: 0;
      padding: 28px;
    }}
    header, main {{
      max-width: 1180px;
      margin: 0 auto;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 28px;
      line-height: 1.2;
      letter-spacing: 0;
    }}
    .summary {{
      margin: 0 0 22px;
      color: #4b5874;
    }}
    .review-card {{
      margin: 18px 0;
      padding: 18px;
      border: 1px solid #d6dbe5;
      border-radius: 8px;
      background: #ffffff;
    }}
    .card-head {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px 16px;
      align-items: baseline;
      justify-content: space-between;
      margin-bottom: 14px;
    }}
    h2 {{
      margin: 0;
      font-size: 20px;
      line-height: 1.25;
      letter-spacing: 0;
    }}
    .meta {{
      color: #56627a;
      font-size: 14px;
    }}
    .evidence-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
      margin: 14px 0;
    }}
    figure {{
      margin: 0;
      padding: 10px;
      border: 1px solid #dde2ea;
      border-radius: 8px;
      background: #fbfcfe;
    }}
    img {{
      display: block;
      width: 100%;
      max-height: 360px;
      object-fit: contain;
      border: 1px solid #e5e8ef;
      background: #ffffff;
    }}
    figcaption {{
      margin-top: 8px;
      color: #56627a;
      font-size: 13px;
    }}
    dl {{
      display: grid;
      grid-template-columns: minmax(120px, 180px) 1fr;
      gap: 8px 12px;
      margin: 12px 0 0;
      font-size: 14px;
    }}
    dt {{
      color: #56627a;
      font-weight: 650;
    }}
    dd {{
      margin: 0;
      overflow-wrap: anywhere;
    }}
    a {{
      color: #1f5fbf;
    }}
    code {{
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 13px;
      background: #eef2f7;
      padding: 2px 5px;
      border-radius: 4px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>CMP Manual Review Packet</h1>
    <p class="summary">{len(rows)} pending review cards. Use these screenshots and DOM links to fill the worksheet decisions.</p>
  </header>
  <main>
{cards}
  </main>
</body>
</html>
"""


def _render_packet_html_card(
    row: dict[str, str],
    *,
    out_dir: Path,
    project_root: Path,
) -> str:
    name = row.get("name") or row.get("url") or "site"
    access_href = _asset_href(row.get("access_screenshot_path", ""), out_dir, project_root)
    capture_href = _asset_href(row.get("capture_screenshot_ref", ""), out_dir, project_root)
    dom_href = _asset_href(row.get("capture_dom_snapshot_ref", ""), out_dir, project_root)
    return f"""    <article class="review-card" id="{escape(_html_id(name))}">
      <div class="card-head">
        <h2>{escape(name)}</h2>
        <div class="meta">{escape(row.get("category", ""))} / {escape(row.get("cohort", ""))} / {escape(row.get("tier", ""))}</div>
      </div>
      <div class="evidence-grid">
        {_html_figure("Access probe", access_href)}
        {_html_figure("Weekly capture", capture_href)}
      </div>
      <dl>
        <dt>URL</dt><dd><a href="{escape(row.get("url", ""))}">{escape(row.get("url", ""))}</a></dd>
        <dt>Review reason</dt><dd>{escape(row.get("review_reason", ""))}</dd>
        <dt>Recommended action</dt><dd>{escape(row.get("recommended_action", ""))}</dd>
        <dt>Decision options</dt><dd><code>{escape(DECISION_OPTIONS)}</code></dd>
        <dt>Capture DOM</dt><dd><a href="{escape(dom_href)}">{escape(row.get("capture_dom_snapshot_ref", ""))}</a></dd>
        <dt>DOM hash</dt><dd><code>{escape(row.get("dom_hash", ""))}</code></dd>
        <dt>Image hash</dt><dd><code>{escape(row.get("image_hash", ""))}</code></dd>
      </dl>
    </article>"""


def _html_figure(label: str, href: str) -> str:
    if not href:
        return f"<figure><figcaption>{escape(label)} missing</figcaption></figure>"
    return (
        f'<figure><img src="{escape(href)}" alt="{escape(label)} screenshot">'
        f"<figcaption>{escape(label)}</figcaption></figure>"
    )


def _render_packet_markdown(
    rows: list[dict[str, str]],
    *,
    out_dir: Path,
    project_root: Path,
) -> str:
    sections = ["# CMP Manual Review Packet", ""]
    sections.append(
        f"{len(rows)} pending review cards. Use these evidence refs to fill the worksheet."
    )
    for row in rows:
        name = row.get("name") or row.get("url") or "site"
        access_href = _asset_href(row.get("access_screenshot_path", ""), out_dir, project_root)
        capture_href = _asset_href(row.get("capture_screenshot_ref", ""), out_dir, project_root)
        dom_href = _asset_href(row.get("capture_dom_snapshot_ref", ""), out_dir, project_root)
        sections.extend(
            [
                "",
                f"## {name}",
                "",
                f"- URL: {row.get('url', '')}",
                f"- Category/cohort/tier: {row.get('category', '')} / {row.get('cohort', '')} / {row.get('tier', '')}",
                f"- Review reason: {row.get('review_reason', '')}",
                f"- Recommended action: {row.get('recommended_action', '')}",
                f"- Decision options: `{DECISION_OPTIONS}`",
                f"- Capture DOM: [Capture DOM]({dom_href})",
                "",
                f"![Access probe]({access_href})",
                "",
                f"![Weekly capture]({capture_href})",
            ]
        )
    return "\n".join(sections) + "\n"


def _asset_href(ref: str, out_dir: Path, project_root: Path) -> str:
    clean_ref = ref.strip()
    if not clean_ref:
        return ""
    if "://" in clean_ref:
        return clean_ref

    ref_path = Path(clean_ref)
    if ref_path.is_absolute():
        source_path = ref_path
    else:
        source_path = project_root / ref_path
        if not source_path.exists() and ref_path.parts[:1] == ("captures",):
            source_path = project_root / "data" / ref_path

    start_path = out_dir if out_dir.is_absolute() else project_root / out_dir
    return Path(os.path.relpath(source_path, start=start_path)).as_posix()


def _html_id(name: str) -> str:
    normalized = sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return normalized or "site"


def _read_latest_by_url(path: Path | Sequence[Path]) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    paths = [path] if isinstance(path, Path) else list(path)
    for one_path in paths:
        with one_path.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                url = (row.get("url") or "").strip()
                if url:
                    rows[_canonicalize_url(url)] = row
    return rows


def _review_reason(
    *,
    access_banner_detected: bool,
    consent_banner_detected: bool,
) -> str:
    if not access_banner_detected and not consent_banner_detected:
        return NO_BANNER_REVIEW_REASON
    return "readiness table requires CMP review; inspect saved evidence before sample lock"


def _canonicalize_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", parsed.query, ""))


def _parse_bool(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y"}


def _format_bool(value: bool) -> str:
    return "true" if value else "false"
