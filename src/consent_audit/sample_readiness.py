"""Build advisor-facing sample readiness tables."""

from __future__ import annotations

import csv
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlparse, urlunparse


@dataclass(frozen=True)
class SampleReadinessRow:
    url: str
    name: str
    category: str
    cohort: str
    candidate_status: str
    selection_reason: str
    access_http_status: int | None
    access_loaded: bool
    access_banner_detected: bool
    access_block_signal: str
    access_screenshot_path: str
    capture_observed: bool
    capture_date: str
    consent_banner_detected: bool
    layer1_gate_passed: bool
    tier: str
    readiness_status: str
    readiness_notes: str


FIELDNAMES = list(SampleReadinessRow.__dataclass_fields__.keys())


def build_sample_readiness(
    candidates_csv: Path,
    access_probe_csv: Path,
    consent_table_csv: Path | Sequence[Path],
) -> list[SampleReadinessRow]:
    access_rows = _read_latest_by_url(access_probe_csv)
    consent_rows = _read_latest_by_url(consent_table_csv)

    rows: list[SampleReadinessRow] = []
    with candidates_csv.open(encoding="utf-8") as fh:
        for candidate in csv.DictReader(fh):
            url = (candidate.get("url") or "").strip()
            if not url or url.startswith("#"):
                continue

            canonical_url = _canonicalize_url(url)
            access = access_rows.get(canonical_url, {})
            consent = consent_rows.get(canonical_url, {})
            http_status = _parse_int(access.get("http_status", ""))
            access_block_signal = (access.get("block_signal") or access.get("error") or "").strip()
            access_loaded = http_status is not None and http_status < 400 and access_block_signal == ""
            access_banner_detected = _parse_bool(access.get("banner_detected", ""))
            capture_observed = bool(consent)
            consent_banner_detected = _parse_bool(consent.get("banner_detected", ""))
            layer1_gate_passed = _parse_bool(consent.get("layer1_gate_passed", ""))

            readiness_status, readiness_notes = _classify_readiness(
                category=(candidate.get("category") or "").strip().lower(),
                access_present=bool(access),
                access_loaded=access_loaded,
                access_block_signal=access_block_signal,
                capture_observed=capture_observed,
                access_banner_detected=access_banner_detected,
                consent_banner_detected=consent_banner_detected,
            )

            rows.append(
                SampleReadinessRow(
                    url=url,
                    name=(candidate.get("name") or "").strip(),
                    category=(candidate.get("category") or "").strip(),
                    cohort=(candidate.get("cohort") or "").strip(),
                    candidate_status=(candidate.get("status") or "").strip(),
                    selection_reason=(candidate.get("selection_reason") or "").strip(),
                    access_http_status=http_status,
                    access_loaded=access_loaded,
                    access_banner_detected=access_banner_detected,
                    access_block_signal=access_block_signal,
                    access_screenshot_path=(access.get("screenshot_path") or "").strip(),
                    capture_observed=capture_observed,
                    capture_date=(consent.get("capture_date") or "").strip(),
                    consent_banner_detected=consent_banner_detected,
                    layer1_gate_passed=layer1_gate_passed,
                    tier=(consent.get("tier") or "").strip(),
                    readiness_status=readiness_status,
                    readiness_notes=readiness_notes,
                )
            )
    return rows


def export_sample_readiness_to_csv(out_csv: Path, rows: list[SampleReadinessRow]) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            record = asdict(row)
            record["access_http_status"] = _format_optional_int(row.access_http_status)
            record["access_loaded"] = _format_bool(row.access_loaded)
            record["access_banner_detected"] = _format_bool(row.access_banner_detected)
            record["capture_observed"] = _format_bool(row.capture_observed)
            record["consent_banner_detected"] = _format_bool(row.consent_banner_detected)
            record["layer1_gate_passed"] = _format_bool(row.layer1_gate_passed)
            writer.writerow(record)


def summarize_readiness(rows: list[SampleReadinessRow]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for row in rows:
        summary[row.readiness_status] = summary.get(row.readiness_status, 0) + 1
    return summary


def _read_latest_by_url(path: Path | Sequence[Path]) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    paths = [path] if isinstance(path, Path) else list(path)
    for one_path in paths:
        with one_path.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                url = (row.get("url") or "").strip()
                if not url:
                    continue
                rows[_canonicalize_url(url)] = row
    return rows


def _classify_readiness(
    *,
    category: str,
    access_present: bool,
    access_loaded: bool,
    access_block_signal: str,
    capture_observed: bool,
    access_banner_detected: bool,
    consent_banner_detected: bool,
) -> tuple[str, str]:
    if not access_present:
        return "needs_access_probe", "no access probe row found"
    if access_block_signal or not access_loaded:
        reason = access_block_signal or "http/load failure"
        return "access_blocked", f"access blocked: {reason}"
    if not capture_observed:
        return "needs_weekly_capture", "access probe exists but no weekly capture row found"
    if not access_banner_detected and not consent_banner_detected:
        if category in {"control", "reference"}:
            return "control_candidate", "no banner observed; keep only as control if intentional"
        return "needs_cmp_review", "no banner observed; verify whether this site fits the consent sample"
    return "pilot_ready", "access and weekly capture available"


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


def _format_optional_int(value: int | None) -> str:
    return "" if value is None else str(value)
