"""Review replacement candidates before promoting them into the deep sample."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlparse, urlunparse


@dataclass(frozen=True)
class ReplacementReviewRow:
    url: str
    name: str
    category: str
    access_loaded: bool
    access_banner_detected: bool
    access_block_signal: str
    access_screenshot_path: str
    capture_observed: bool
    capture_date: str
    consent_banner_detected: bool
    layer1_gate_passed: bool
    accept_available: bool
    reject_available: bool
    customize_available: bool
    tier: str
    replacement_status: str
    priority: int
    recommended_action: str
    evidence_notes: str


FIELDNAMES = list(ReplacementReviewRow.__dataclass_fields__.keys())
WEEKLY_TARGET_FIELDNAMES = [
    "url",
    "name",
    "category",
    "inherited_from_phd_mentor",
    "notes",
]


def build_replacement_review(
    candidates_csv: Path,
    access_probe_csv: Path,
    consent_table_csv: Path,
) -> list[ReplacementReviewRow]:
    """Merge replacement evidence and classify sample-lock readiness."""
    access_rows = _read_latest_by_url(access_probe_csv)
    consent_rows = _read_latest_by_url(consent_table_csv)
    rows: list[ReplacementReviewRow] = []

    with candidates_csv.open(encoding="utf-8") as fh:
        for candidate in csv.DictReader(fh):
            url = (candidate.get("url") or "").strip()
            if not url or url.startswith("#"):
                continue
            canonical_url = _canonicalize_url(url)
            access = access_rows.get(canonical_url, {})
            consent = consent_rows.get(canonical_url, {})

            http_status = _parse_int(access.get("http_status", ""))
            access_block_signal = (
                access.get("block_signal") or access.get("error") or ""
            ).strip()
            access_loaded = (
                http_status is not None
                and http_status < 400
                and access_block_signal == ""
            )
            access_banner_detected = _parse_bool(access.get("banner_detected", ""))
            capture_observed = bool(consent)
            consent_banner_detected = _parse_bool(consent.get("banner_detected", ""))
            layer1_gate_passed = _parse_bool(consent.get("layer1_gate_passed", ""))
            accept_available = _parse_bool(consent.get("accept_available", ""))
            reject_available = _parse_bool(consent.get("reject_available", ""))
            customize_available = _parse_bool(consent.get("customize_available", ""))

            status, priority, action, notes = _classify_replacement(
                access_present=bool(access),
                access_loaded=access_loaded,
                access_block_signal=access_block_signal,
                access_banner_detected=access_banner_detected,
                capture_observed=capture_observed,
                consent_banner_detected=consent_banner_detected,
                layer1_gate_passed=layer1_gate_passed,
                accept_available=accept_available,
                reject_available=reject_available,
                customize_available=customize_available,
            )

            rows.append(
                ReplacementReviewRow(
                    url=url,
                    name=(candidate.get("name") or "").strip(),
                    category=(candidate.get("category") or "").strip(),
                    access_loaded=access_loaded,
                    access_banner_detected=access_banner_detected,
                    access_block_signal=access_block_signal,
                    access_screenshot_path=(access.get("screenshot_path") or "").strip(),
                    capture_observed=capture_observed,
                    capture_date=(consent.get("capture_date") or "").strip(),
                    consent_banner_detected=consent_banner_detected,
                    layer1_gate_passed=layer1_gate_passed,
                    accept_available=accept_available,
                    reject_available=reject_available,
                    customize_available=customize_available,
                    tier=(consent.get("tier") or "").strip(),
                    replacement_status=status,
                    priority=priority,
                    recommended_action=action,
                    evidence_notes=notes,
                )
            )

    return rows


def export_replacement_review_to_csv(
    out_csv: Path,
    rows: list[ReplacementReviewRow],
) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            record = asdict(row)
            for field in [
                "access_loaded",
                "access_banner_detected",
                "capture_observed",
                "consent_banner_detected",
                "layer1_gate_passed",
                "accept_available",
                "reject_available",
                "customize_available",
            ]:
                record[field] = _format_bool(record[field])
            record["priority"] = str(row.priority)
            writer.writerow(record)


def summarize_replacement_review(rows: list[ReplacementReviewRow]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for row in rows:
        summary[row.replacement_status] = summary.get(row.replacement_status, 0) + 1
    return summary


def export_expanded_weekly_targets(
    base_targets_csv: Path,
    replacement_review_csv: Path,
    out_csv: Path,
) -> int:
    """Merge verified replacements into the current weekly target site list."""
    targets = _read_site_targets(base_targets_csv)
    seen = {_canonicalize_url(row["url"]) for row in targets}

    with replacement_review_csv.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            url = (row.get("url") or "").strip()
            if not url or (row.get("replacement_status") or "").strip() != "verified_replacement":
                continue
            canonical_url = _canonicalize_url(url)
            if canonical_url in seen:
                continue
            seen.add(canonical_url)
            targets.append(
                {
                    "url": url,
                    "name": (row.get("name") or "").strip(),
                    "category": (row.get("category") or "").strip(),
                    "inherited_from_phd_mentor": "false",
                    "notes": (
                        "verified_replacement: "
                        f"{(row.get('recommended_action') or '').strip()}"
                    ),
                }
            )

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=WEEKLY_TARGET_FIELDNAMES)
        writer.writeheader()
        writer.writerows(targets)
    return len(targets)


def _classify_replacement(
    *,
    access_present: bool,
    access_loaded: bool,
    access_block_signal: str,
    access_banner_detected: bool,
    capture_observed: bool,
    consent_banner_detected: bool,
    layer1_gate_passed: bool,
    accept_available: bool,
    reject_available: bool,
    customize_available: bool,
) -> tuple[str, int, str, str]:
    if not access_present:
        return (
            "needs_access_probe",
            2,
            "run access probe before any sample-lock promotion",
            "no access probe row found",
        )
    if access_block_signal or not access_loaded:
        reason = access_block_signal or "http/load failure"
        return (
            "blocked_or_error",
            4,
            "avoid unless intentionally kept as access-friction evidence",
            f"access blocked: {reason}",
        )
    if not access_banner_detected and not consent_banner_detected:
        return (
            "no_banner_or_locale_shift",
            3,
            "do not use as banner-present replacement unless kept as contrast case",
            "no banner observed in access probe or weekly capture",
        )
    if not capture_observed:
        return (
            "needs_weekly_capture",
            2,
            "run full weekly capture before sample-lock promotion",
            "access probe exists but no weekly capture row found",
        )
    if (
        layer1_gate_passed
        and accept_available
        and reject_available
        and customize_available
    ):
        return (
            "verified_replacement",
            1,
            "add to expanded weekly capture shortlist pending advisor confirmation",
            "full weekly capture reproduced Accept, Reject, and Customize paths",
        )
    return (
        "promising_reprobe",
        2,
        "reprobe with fresh context before any sample-lock promotion",
        "access banner hit did not reproduce a full Layer 1 pass",
    )


def _read_latest_by_url(path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            url = (row.get("url") or "").strip()
            if url:
                rows[_canonicalize_url(url)] = row
    return rows


def _read_site_targets(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as fh:
        rows = []
        for row in csv.DictReader(fh):
            url = (row.get("url") or "").strip()
            if not url:
                continue
            rows.append(
                {
                    "url": url,
                    "name": (row.get("name") or "").strip(),
                    "category": (row.get("category") or "").strip(),
                    "inherited_from_phd_mentor": (
                        row.get("inherited_from_phd_mentor") or "false"
                    ).strip(),
                    "notes": (row.get("notes") or "").strip(),
                }
            )
    return rows


def _canonicalize_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", parsed.query, ""))


def _parse_bool(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y"}


def _format_bool(value: bool) -> str:
    return "true" if value else "false"


def _parse_int(value: str | None) -> int | None:
    try:
        return int((value or "").strip())
    except ValueError:
        return None
