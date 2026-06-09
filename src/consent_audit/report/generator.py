"""Human-readable report from structured layer results.

Critical: every claim in the report text must cite an evidence ref from the underlying
schema (ElementRef or ScreenshotBBox). This is the anti-hallucination discipline
from AGENTS.md §2 principle 1.
"""

from datetime import UTC, datetime

from consent_audit.models import (
    AuditReport,
    CaptureBundle,
    EffortCategory,
    Layer1Result,
    Layer2Result,
    Layer3Result,
    LetterGrade,
    Tier,
)

_GRADE_RANK = {
    LetterGrade.A: 5,
    LetterGrade.B: 4,
    LetterGrade.C: 3,
    LetterGrade.D: 2,
    LetterGrade.F: 1,
}


def generate_report(
    bundle: CaptureBundle,
    layer1: Layer1Result,
    layer2: Layer2Result | None,
    layer3: Layer3Result | None,
    *,
    api_cost_usd: float,
) -> AuditReport:
    """Assemble the final AuditReport with Markdown body + tier classification."""
    tier = classify_tier(layer1, layer2, layer3)
    generated_at = datetime.now(UTC)
    report_markdown = _render_markdown(
        bundle=bundle,
        layer1=layer1,
        layer2=layer2,
        layer3=layer3,
        tier=tier,
        api_cost_usd=api_cost_usd,
        generated_at=generated_at,
    )
    return AuditReport(
        bundle=bundle,
        layer1=layer1,
        layer2=layer2,
        layer3=layer3,
        tier=tier,
        report_markdown=report_markdown,
        total_api_cost_usd=api_cost_usd,
        generated_at=generated_at,
    )


def classify_tier(
    layer1: Layer1Result,
    layer2: Layer2Result | None,
    layer3: Layer3Result | None,
) -> Tier:
    """Map layer results to the four-tier categorical summary (CONCEPTS.md §4)."""
    if not layer1.gate_passed or layer2 is None or layer3 is None:
        return Tier.HIGH_RISK

    transparency = layer3.transparency.letter_grade
    unbiased = layer3.unbiased_choice.letter_grade

    if (
        layer2.overall_category == EffortCategory.EASY
        and _at_least(transparency, LetterGrade.B)
        and _at_least(unbiased, LetterGrade.B)
        and layer1.accept_available
        and layer1.reject_available
        and layer1.customize_available
        and layer1.dismiss_available
    ):
        return Tier.EXEMPLARY

    if (
        layer2.overall_category == EffortCategory.POOR
        and (not _at_least(transparency, LetterGrade.C) or not _at_least(unbiased, LetterGrade.C))
    ):
        return Tier.HIGH_RISK

    if (
        layer2.overall_category == EffortCategory.POOR
        or transparency == LetterGrade.D
        or unbiased == LetterGrade.D
    ):
        return Tier.MARGINAL

    if (
        layer2.overall_category in {EffortCategory.EASY, EffortCategory.AVERAGE}
        and _at_least(transparency, LetterGrade.C)
        and _at_least(unbiased, LetterGrade.C)
    ):
        return Tier.COMPLIANT

    return Tier.MARGINAL


def _at_least(actual: LetterGrade, minimum: LetterGrade) -> bool:
    return _GRADE_RANK[actual] >= _GRADE_RANK[minimum]


def _render_markdown(
    *,
    bundle: CaptureBundle,
    layer1: Layer1Result,
    layer2: Layer2Result | None,
    layer3: Layer3Result | None,
    tier: Tier,
    api_cost_usd: float,
    generated_at: datetime,
) -> str:
    lines = [
        f"# Consent Interface Audit: {bundle.url}",
        "",
        f"- Generated at: {generated_at.isoformat()}Z",
        f"- Tier: {tier.value}",
        f"- API cost: ${api_cost_usd:.4f}",
        "",
        "## Layer 1 — Path Availability",
        "",
        f"- Accept available: {layer1.accept_available}",
        f"- Reject available: {layer1.reject_available}",
        f"- Customize available: {layer1.customize_available}",
        f"- Dismiss available: {layer1.dismiss_available}",
        f"- Gate passed: {layer1.gate_passed}",
    ]
    if layer1.missing_paths:
        missing = ", ".join(path.value for path in layer1.missing_paths)
        lines.append(f"- Missing paths: {missing}")

    if layer2 is not None:
        lines.extend(
            [
                "",
                "## Layer 2 — Path Effort",
                "",
                f"- Overall category: {layer2.overall_category.value}",
                f"- Mean effort: {layer2.mean_effort:.3f}",
            ]
        )

    if layer3 is not None:
        lines.extend(
            [
                "",
                "## Layer 3 — Transparency & Unbiased Choice",
                "",
                f"- Transparency grade: {layer3.transparency.letter_grade.value}",
                f"- Unbiased-choice grade: {layer3.unbiased_choice.letter_grade.value}",
            ]
        )
        if layer3.transparency.topic_coverage:
            lines.extend(["", "### Disclosure Topic Coverage", ""])
            for topic_result in sorted(
                layer3.transparency.topic_coverage.values(),
                key=lambda result: result.topic.value,
            ):
                lines.append(
                    "- "
                    f"{topic_result.topic.value}: "
                    f"present={topic_result.present}, "
                    f"grade={topic_result.clarity_grade.value}, "
                    f"quote={_quote_or_none(topic_result.evidence_quote)}"
                )

        if layer3.transparency.framing:
            lines.extend(["", "### Communicative Framing", ""])
            for framing_result in sorted(
                layer3.transparency.framing.values(),
                key=lambda result: result.mechanism.value,
            ):
                lines.append(
                    "- "
                    f"{framing_result.mechanism.value}: "
                    f"level={framing_result.level.value}; "
                    f"{framing_result.rationale}"
                )
                for evidence_quote in framing_result.evidence_quotes:
                    lines.append(f"  - quote={_quote_or_none(evidence_quote)}")

        lines.extend(
            [
                "",
                "### Unbiased Choice",
                "",
                f"- Asymmetry score: {layer3.unbiased_choice.asymmetry_score:.3f}",
                f"- Biased toward: {_pathway_or_none(layer3.unbiased_choice.biased_toward)}",
                f"- Rationale: {layer3.unbiased_choice.rationale}",
            ]
        )

    return "\n".join(lines) + "\n"


def _quote_or_none(value: str | None) -> str:
    if value is None:
        return "None"
    return f'"{value}"'


def _pathway_or_none(pathway: object | None) -> str:
    if pathway is None:
        return "none"
    value = getattr(pathway, "value", None)
    return str(value if value is not None else pathway)
