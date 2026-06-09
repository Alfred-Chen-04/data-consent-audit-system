"""One-command export for the SSRP research data package."""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from consent_audit.audit_export import export_audit_reports_to_csv
from consent_audit.longitudinal_export import export_weekly_summaries_to_csv
from consent_audit.storage import list_reports, list_weekly_summaries


def export_research_package(out_dir: Path, *, limit: int = 500) -> dict[str, Any]:
    """Write all paper-facing tables plus a manifest."""
    out_dir.mkdir(parents=True, exist_ok=True)
    audit_csv = out_dir / "audit_report_summary.csv"
    longitudinal_csv = out_dir / "longitudinal_summary.csv"
    manifest_path = out_dir / "research_manifest.json"

    reports = list_reports(limit=limit)
    summaries = list_weekly_summaries(limit=limit)

    export_audit_reports_to_csv(audit_csv, reports)
    export_weekly_summaries_to_csv(longitudinal_csv, summaries)

    manifest: dict[str, Any] = {
        "generated_at": datetime.now(UTC).isoformat(),
        "audit_report_count": len(reports),
        "weekly_summary_count": len(summaries),
        "files": {
            "audit_report_summary": audit_csv.name,
            "longitudinal_summary": longitudinal_csv.name,
        },
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest
