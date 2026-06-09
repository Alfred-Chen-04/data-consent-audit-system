"""Paper-facing exports for cross-sectional AuditReport results."""

import csv
from pathlib import Path

from consent_audit.models import AuditReport

AUDIT_REPORT_FIELDNAMES = [
    "report_id",
    "bundle_id",
    "url",
    "capture_date",
    "captured_at",
    "generated_at",
    "banner_detected",
    "tier",
    "layer1_gate_passed",
    "accept_available",
    "reject_available",
    "customize_available",
    "dismiss_available",
    "missing_paths",
    "layer2_mean_effort",
    "layer2_overall_category",
    "transparency_grade",
    "unbiased_choice_grade",
    "biased_toward",
    "first_screenshot_ref",
    "first_dom_snapshot_ref",
    "dom_hash",
    "image_hash",
    "api_cost_usd",
]


def audit_report_to_row(report: AuditReport) -> dict[str, str]:
    """Flatten an AuditReport into one stable CSV row."""
    first_layer = report.bundle.layers[0] if report.bundle.layers else None
    layer2 = report.layer2
    layer3 = report.layer3
    return {
        "report_id": str(report.report_id),
        "bundle_id": str(report.bundle.bundle_id),
        "url": str(report.bundle.url),
        "capture_date": report.bundle.captured_at.date().isoformat(),
        "captured_at": report.bundle.captured_at.isoformat(),
        "generated_at": report.generated_at.isoformat(),
        "banner_detected": _bool_cell(
            any(outcome.attempted for outcome in report.bundle.path_outcomes.values())
        ),
        "tier": report.tier.value,
        "layer1_gate_passed": _bool_cell(report.layer1.gate_passed),
        "accept_available": _bool_cell(report.layer1.accept_available),
        "reject_available": _bool_cell(report.layer1.reject_available),
        "customize_available": _bool_cell(report.layer1.customize_available),
        "dismiss_available": _bool_cell(report.layer1.dismiss_available),
        "missing_paths": "|".join(pathway.value for pathway in report.layer1.missing_paths),
        "layer2_mean_effort": f"{layer2.mean_effort:.2f}" if layer2 is not None else "",
        "layer2_overall_category": layer2.overall_category.value if layer2 is not None else "",
        "transparency_grade": (
            layer3.transparency.letter_grade.value if layer3 is not None else ""
        ),
        "unbiased_choice_grade": (
            layer3.unbiased_choice.letter_grade.value if layer3 is not None else ""
        ),
        "biased_toward": (
            layer3.unbiased_choice.biased_toward.value
            if layer3 is not None and layer3.unbiased_choice.biased_toward is not None
            else ""
        ),
        "first_screenshot_ref": first_layer.screenshot_ref if first_layer is not None else "",
        "first_dom_snapshot_ref": first_layer.dom_snapshot_ref if first_layer is not None else "",
        "dom_hash": report.bundle.fingerprint.dom_hash,
        "image_hash": report.bundle.fingerprint.perceptual_image_hash,
        "api_cost_usd": f"{report.total_api_cost_usd:.4f}",
    }


def export_audit_reports_to_csv(path: Path, reports: list[AuditReport]) -> None:
    """Write AuditReport rows as a research-ready CSV table."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=AUDIT_REPORT_FIELDNAMES)
        writer.writeheader()
        for report in reports:
            writer.writerow(audit_report_to_row(report))


def _bool_cell(value: bool) -> str:
    return "true" if value else "false"
