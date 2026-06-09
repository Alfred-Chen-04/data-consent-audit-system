"""Tests for deterministic Layer 3 transparency and unbiased-choice scoring."""

from datetime import UTC, datetime

from consent_audit.layers import score_layer1, score_layer2, score_layer3
from consent_audit.models import (
    BiasLevel,
    CaptureBundle,
    DisclosureTopic,
    EffortCategory,
    EffortScore,
    ElementRef,
    FramingMechanism,
    Layer2Result,
    LayerSnapshot,
    LetterGrade,
    MultimodalFingerprint,
    PathOutcome,
    Pathway,
)


def _element(pathway: Pathway) -> ElementRef:
    return ElementRef(dom_selector=f"button.{pathway.value}", visible_text=pathway.value.title())


def _bundle(text: str) -> CaptureBundle:
    return CaptureBundle(
        url="https://example.com",  # type: ignore[arg-type]
        captured_at=datetime(2026, 5, 30, tzinfo=UTC),
        layers=[
            LayerSnapshot(
                layer_index=1,
                screenshot_ref="captures/example/layer1.png",
                dom_snapshot_ref="captures/example/layer1.html",
                visible_text=text,
            )
        ],
        path_outcomes={
            pathway: PathOutcome(
                pathway=pathway,
                attempted=True,
                succeeded=True,
                click_depth=1,
                trigger_element=_element(pathway),
            )
            for pathway in Pathway
        },
        fingerprint=MultimodalFingerprint(dom_hash="dom", perceptual_image_hash="img"),
    )


def _score(text: str):
    bundle = _bundle(text)
    layer1 = score_layer1(bundle)
    layer2 = score_layer2(bundle, layer1)
    return bundle, score_layer3(bundle, layer1, layer2)


def test_score_layer3_topic_coverage_uses_verbatim_source_quotes() -> None:
    text = (
        "We use cookies and device identifiers for analytics, personalised advertising, "
        "and content measurement. We share data with advertising partners. "
        "You can accept, reject, or customize these choices at any time."
    )

    bundle, result = _score(text)
    source_text = "\n".join(layer.visible_text for layer in bundle.layers)

    assert result.transparency.topic_coverage[DisclosureTopic.DATA_TYPES].present
    assert result.transparency.topic_coverage[DisclosureTopic.PURPOSES].present
    assert result.transparency.topic_coverage[DisclosureTopic.THIRD_PARTY_SHARING].present
    assert result.transparency.topic_coverage[DisclosureTopic.CONSEQUENCES].present
    assert result.transparency.letter_grade in {LetterGrade.A, LetterGrade.B}

    for topic_result in result.transparency.topic_coverage.values():
        assert topic_result.evidence_quote is not None
        assert topic_result.evidence_quote in source_text


def test_score_layer3_absent_topics_do_not_get_hallucinated_quotes() -> None:
    text = "Accept cookies to support us and improve your experience. By continuing you agree."

    _, result = _score(text)

    sharing = result.transparency.topic_coverage[DisclosureTopic.THIRD_PARTY_SHARING]
    assert not sharing.present
    assert sharing.clarity_grade == LetterGrade.F
    assert sharing.evidence_quote is None
    assert (
        result.transparency.framing[FramingMechanism.SELECTIVE_PROMINENCE].level
        != BiasLevel.NEUTRAL
    )
    assert result.transparency.letter_grade in {LetterGrade.D, LetterGrade.F}


def test_score_layer3_unbiased_choice_penalizes_accept_shortcut() -> None:
    bundle = _bundle(
        "We use cookies and device identifiers for analytics. "
        "We share data with advertising partners. Accept, reject, or customize choices."
    )
    layer1 = score_layer1(bundle)
    layer2 = Layer2Result(
        per_path_effort={
            Pathway.ACCEPT: EffortScore(pathway=Pathway.ACCEPT, sub_features=[], score=0.0),
            Pathway.REJECT: EffortScore(pathway=Pathway.REJECT, sub_features=[], score=0.6),
            Pathway.CUSTOMIZE: EffortScore(
                pathway=Pathway.CUSTOMIZE,
                sub_features=[],
                score=0.6,
            ),
        },
        overall_category=EffortCategory.AVERAGE,
        mean_effort=0.4,
    )

    result = score_layer3(bundle, layer1, layer2)

    assert result.unbiased_choice.biased_toward == Pathway.ACCEPT
    assert result.unbiased_choice.asymmetry_score >= 0.4
    assert result.unbiased_choice.letter_grade in {LetterGrade.C, LetterGrade.D}
