"""Tests for report tiering and minimal report assembly."""

from datetime import datetime

from consent_audit.models import (
    BiasLevel,
    CaptureBundle,
    DisclosureTopic,
    EffortCategory,
    FramingMechanism,
    Layer1Result,
    Layer2Result,
    LetterGrade,
    MultimodalFingerprint,
    Pathway,
    Tier,
)
from consent_audit.models.audit import (
    FramingResult,
    Layer3Result,
    TopicCoverageResult,
    TransparencyResult,
    UnbiasedChoiceResult,
)
from consent_audit.report.generator import classify_tier, generate_report


def _layer1(*, gate_passed: bool = True) -> Layer1Result:
    return Layer1Result(
        accept_available=True,
        reject_available=gate_passed,
        customize_available=gate_passed,
        dismiss_available=True,
        missing_paths=[] if gate_passed else [Pathway.REJECT],
        evidence={},
        gate_passed=gate_passed,
    )


def _layer2(category: EffortCategory, mean_effort: float) -> Layer2Result:
    return Layer2Result(per_path_effort={}, overall_category=category, mean_effort=mean_effort)


def _layer3(transparency: LetterGrade, unbiased: LetterGrade) -> Layer3Result:
    return Layer3Result(
        transparency=TransparencyResult(
            topic_coverage={},
            framing={},
            letter_grade=transparency,
            rationale="fixture",
        ),
        unbiased_choice=UnbiasedChoiceResult(
            asymmetry_score=0.1,
            biased_toward=None,
            evidence=[],
            letter_grade=unbiased,
            rationale="fixture",
        ),
    )


def _layer3_with_evidence() -> Layer3Result:
    quote = "We share data with advertising partners."
    return Layer3Result(
        transparency=TransparencyResult(
            topic_coverage={
                DisclosureTopic.THIRD_PARTY_SHARING: TopicCoverageResult(
                    topic=DisclosureTopic.THIRD_PARTY_SHARING,
                    present=True,
                    clarity_grade=LetterGrade.B,
                    evidence_quote=quote,
                ),
                DisclosureTopic.CONSEQUENCES: TopicCoverageResult(
                    topic=DisclosureTopic.CONSEQUENCES,
                    present=False,
                    clarity_grade=LetterGrade.F,
                    evidence_quote=None,
                ),
            },
            framing={
                FramingMechanism.SELECTIVE_PROMINENCE: FramingResult(
                    mechanism=FramingMechanism.SELECTIVE_PROMINENCE,
                    level=BiasLevel.STRONG_BIAS,
                    rationale="Benefit language appears without reject consequences.",
                    evidence_quotes=["Accept cookies to support us."],
                )
            },
            letter_grade=LetterGrade.D,
            rationale="fixture transparency rationale",
        ),
        unbiased_choice=UnbiasedChoiceResult(
            asymmetry_score=0.45,
            biased_toward=Pathway.ACCEPT,
            evidence=[],
            letter_grade=LetterGrade.C,
            rationale="Accept is easier than reject.",
        ),
    )


def test_classify_tier_high_risk_when_layer1_gate_fails() -> None:
    assert classify_tier(_layer1(gate_passed=False), None, None) == Tier.HIGH_RISK


def test_classify_tier_exemplary_for_easy_high_grades() -> None:
    assert (
        classify_tier(
            _layer1(),
            _layer2(EffortCategory.EASY, 0.2),
            _layer3(LetterGrade.A, LetterGrade.B),
        )
        == Tier.EXEMPLARY
    )


def test_classify_tier_marginal_for_poor_effort_without_low_grades() -> None:
    assert (
        classify_tier(
            _layer1(),
            _layer2(EffortCategory.POOR, 0.8),
            _layer3(LetterGrade.B, LetterGrade.B),
        )
        == Tier.MARGINAL
    )


def test_generate_report_returns_audit_report_with_markdown_summary() -> None:
    bundle = CaptureBundle(
        url="https://example.com",  # type: ignore[arg-type]
        captured_at=datetime(2026, 5, 30),
        layers=[],
        path_outcomes={},
        fingerprint=MultimodalFingerprint(dom_hash="dom", perceptual_image_hash="img"),
    )

    report = generate_report(
        bundle,
        _layer1(gate_passed=False),
        None,
        None,
        api_cost_usd=0.0,
    )

    assert report.tier == Tier.HIGH_RISK
    assert "https://example.com/" in report.report_markdown
    assert "Layer 1" in report.report_markdown


def test_generate_report_renders_layer3_evidence_cards() -> None:
    bundle = CaptureBundle(
        url="https://example.com",  # type: ignore[arg-type]
        captured_at=datetime(2026, 5, 30),
        layers=[],
        path_outcomes={},
        fingerprint=MultimodalFingerprint(dom_hash="dom", perceptual_image_hash="img"),
    )

    report = generate_report(
        bundle,
        _layer1(),
        _layer2(EffortCategory.AVERAGE, 0.4),
        _layer3_with_evidence(),
        api_cost_usd=0.0,
    )

    assert "### Disclosure Topic Coverage" in report.report_markdown
    assert "third_party_sharing" in report.report_markdown
    assert "present=True" in report.report_markdown
    assert '"We share data with advertising partners."' in report.report_markdown
    assert "consequences" in report.report_markdown
    assert "quote=None" in report.report_markdown
    assert "### Communicative Framing" in report.report_markdown
    assert "selective_prominence" in report.report_markdown
    assert '"Accept cookies to support us."' in report.report_markdown
    assert "### Unbiased Choice" in report.report_markdown
    assert "Biased toward: accept" in report.report_markdown
