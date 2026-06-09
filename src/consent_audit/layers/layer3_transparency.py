"""Layer 3 — Transparency and Unbiased Choice. Two analytically distinct scores.

CONCEPTS.md §3 forbids collapsing these into one number.
"""

import re
from collections.abc import Iterable

from consent_audit.models import (
    BiasLevel,
    CaptureBundle,
    DisclosureTopic,
    ElementRef,
    FramingMechanism,
    FramingResult,
    Layer1Result,
    Layer2Result,
    Layer3Result,
    LetterGrade,
    Pathway,
    TopicCoverageResult,
    TransparencyResult,
    UnbiasedChoiceResult,
)

_TOPIC_PATTERNS: dict[DisclosureTopic, tuple[str, ...]] = {
    DisclosureTopic.DATA_TYPES: (
        "cookies?",
        "device identifiers?",
        "personal data",
        "personal information",
        "browsing data",
        "information about you",
    ),
    DisclosureTopic.PURPOSES: (
        "analytics?",
        "advertis(?:e|ing|ement)",
        "personalised",
        "personalized",
        "measurement",
        "improve",
        "support us",
        "content measurement",
    ),
    DisclosureTopic.THIRD_PARTY_SHARING: (
        "share data",
        "third parties",
        "third-party",
        "partners?",
        "advertisers?",
        "vendors?",
        "affiliates?",
    ),
    DisclosureTopic.CONSEQUENCES: (
        r"accept[^.?!]{0,80}reject",
        r"reject[^.?!]{0,80}accept",
        r"accept[^.?!]{0,80}customi[sz]e",
        "choices?",
        "withdraw",
        "necessary cookies only",
    ),
}

_GRADE_SCORE = {
    LetterGrade.A: 4.0,
    LetterGrade.B: 3.0,
    LetterGrade.C: 2.0,
    LetterGrade.D: 1.0,
    LetterGrade.F: 0.0,
}

_GRADE_ORDER = [
    LetterGrade.A,
    LetterGrade.B,
    LetterGrade.C,
    LetterGrade.D,
    LetterGrade.F,
]


def score_layer3(
    bundle: CaptureBundle,
    layer1: Layer1Result,
    layer2: Layer2Result,
) -> Layer3Result:
    """Produce Transparency (topic coverage + framing) AND Unbiased Choice (visual asymmetry).

    Deterministic MVP. LLM/VLM extraction can later replace the heuristics, but
    the final schema and quote validation discipline remain the same.
    """
    source_text = _visible_text(bundle)
    topic_coverage = _score_topic_coverage(source_text)
    framing = _score_framing(source_text)
    transparency_grade = _transparency_grade(topic_coverage.values(), framing.values())

    return Layer3Result(
        transparency=TransparencyResult(
            topic_coverage=topic_coverage,
            framing=framing,
            letter_grade=transparency_grade,
            rationale=(
                "Deterministic Layer 3 MVP from visible first/second-layer text; "
                "all positive topic findings use verbatim evidence quotes."
            ),
        ),
        unbiased_choice=_score_unbiased_choice(layer1, layer2),
    )


def _visible_text(bundle: CaptureBundle) -> str:
    return "\n".join(layer.visible_text for layer in bundle.layers).strip()


def _score_topic_coverage(text: str) -> dict[DisclosureTopic, TopicCoverageResult]:
    return {
        topic: _topic_result(text, topic, patterns)
        for topic, patterns in _TOPIC_PATTERNS.items()
    }


def _topic_result(
    text: str,
    topic: DisclosureTopic,
    patterns: tuple[str, ...],
) -> TopicCoverageResult:
    quote = _first_sentence_matching(text, patterns)
    if quote is None:
        return TopicCoverageResult(
            topic=topic,
            present=False,
            clarity_grade=LetterGrade.F,
            evidence_quote=None,
            evidence_ref=None,
            consistent_with_layer2=None,
        )

    return TopicCoverageResult(
        topic=topic,
        present=True,
        clarity_grade=_clarity_grade(topic, quote),
        evidence_quote=quote,
        evidence_ref=ElementRef(dom_selector="visible_text", visible_text=quote),
        consistent_with_layer2=None,
    )


def _clarity_grade(topic: DisclosureTopic, quote: str) -> LetterGrade:
    normalized = _normalize(quote)
    if re.search(r"\b(may|selected|some|certain|various|including but not limited)\b", normalized):
        return LetterGrade.C

    if topic == DisclosureTopic.DATA_TYPES and _count_matches(
        normalized,
        ("cookie", "identifier", "personal data", "browsing", "device"),
    ) >= 2:
        return LetterGrade.A
    if topic == DisclosureTopic.PURPOSES and _count_matches(
        normalized,
        ("analytics", "advertis", "personal", "measurement", "improve"),
    ) >= 2:
        return LetterGrade.A

    return LetterGrade.B


def _score_framing(text: str) -> dict[FramingMechanism, FramingResult]:
    normalized = _normalize(text)
    benefit_quote = _first_sentence_matching(
        text,
        ("improve your experience", "support us", "better experience", "personalised"),
    )
    control_quote = _first_sentence_matching(
        text,
        ("reject", "decline", "withdraw", "privacy choices", "share data", "tracking"),
    )

    emphasis_level = BiasLevel.NEUTRAL
    if benefit_quote is not None and control_quote is None:
        emphasis_level = BiasLevel.MILD_BIAS

    sequencing_level = BiasLevel.NEUTRAL
    if benefit_quote is not None and _starts_with_benefit(normalized):
        sequencing_level = BiasLevel.MILD_BIAS

    selective_level = BiasLevel.NEUTRAL
    if benefit_quote is not None and control_quote is None:
        selective_level = BiasLevel.STRONG_BIAS

    complexity_level = (
        BiasLevel.MILD_BIAS if _longest_sentence_word_count(text) >= 35 else BiasLevel.NEUTRAL
    )

    return {
        FramingMechanism.EMPHASIS: FramingResult(
            mechanism=FramingMechanism.EMPHASIS,
            level=emphasis_level,
            rationale="Benefit language appears without nearby risk/control language."
            if emphasis_level != BiasLevel.NEUTRAL
            else "No one-sided benefit emphasis detected by the deterministic rubric.",
            evidence_quotes=[benefit_quote] if emphasis_level != BiasLevel.NEUTRAL and benefit_quote else [],
        ),
        FramingMechanism.LINGUISTIC_COMPLEXITY: FramingResult(
            mechanism=FramingMechanism.LINGUISTIC_COMPLEXITY,
            level=complexity_level,
            rationale="A consent sentence exceeds the deterministic complexity threshold."
            if complexity_level != BiasLevel.NEUTRAL
            else "No high-complexity sentence detected by the deterministic rubric.",
            evidence_quotes=[_longest_sentence(text)] if complexity_level != BiasLevel.NEUTRAL else [],
        ),
        FramingMechanism.SEQUENCING: FramingResult(
            mechanism=FramingMechanism.SEQUENCING,
            level=sequencing_level,
            rationale="The first sentence leads with acceptance benefits."
            if sequencing_level != BiasLevel.NEUTRAL
            else "The deterministic rubric did not detect benefit-first sequencing.",
            evidence_quotes=[benefit_quote] if sequencing_level != BiasLevel.NEUTRAL and benefit_quote else [],
        ),
        FramingMechanism.SELECTIVE_PROMINENCE: FramingResult(
            mechanism=FramingMechanism.SELECTIVE_PROMINENCE,
            level=selective_level,
            rationale="Positive outcomes are stated while reject/control consequences are absent."
            if selective_level != BiasLevel.NEUTRAL
            else "The deterministic rubric did not detect selective benefit prominence.",
            evidence_quotes=[benefit_quote] if selective_level != BiasLevel.NEUTRAL and benefit_quote else [],
        ),
    }


def _transparency_grade(
    topics: Iterable[TopicCoverageResult],
    framing: Iterable[FramingResult],
) -> LetterGrade:
    topic_results = list(topics)
    mean_score = sum(_GRADE_SCORE[result.clarity_grade] for result in topic_results) / len(
        topic_results
    )
    if mean_score >= 3.5:
        grade = LetterGrade.A
    elif mean_score >= 2.75:
        grade = LetterGrade.B
    elif mean_score >= 1.5:
        grade = LetterGrade.C
    elif mean_score >= 0.75:
        grade = LetterGrade.D
    else:
        grade = LetterGrade.F

    framing_results = list(framing)
    if any(result.level == BiasLevel.STRONG_BIAS for result in framing_results) or sum(result.level == BiasLevel.MILD_BIAS for result in framing_results) >= 2:
        grade = _drop_grade(grade)
    return grade


def _score_unbiased_choice(
    layer1: Layer1Result,
    layer2: Layer2Result,
) -> UnbiasedChoiceResult:
    accept_effort = _path_effort(layer2, Pathway.ACCEPT)
    reject_effort = _path_effort(layer2, Pathway.REJECT)
    customize_effort = _path_effort(layer2, Pathway.CUSTOMIZE)
    comparison_efforts = [value for value in (reject_effort, customize_effort) if value is not None]

    asymmetry_score = 0.0
    biased_toward: Pathway | None = None
    if accept_effort is not None and comparison_efforts:
        asymmetry_score = max(0.0, min(comparison_efforts) - accept_effort)
        if asymmetry_score > 0.15:
            biased_toward = Pathway.ACCEPT

    return UnbiasedChoiceResult(
        asymmetry_score=round(asymmetry_score, 6),
        biased_toward=biased_toward,
        evidence=list(layer1.evidence.values()),
        letter_grade=_asymmetry_grade(asymmetry_score),
        rationale=(
            "Deterministic MVP uses pathway effort asymmetry until VLM visual "
            "features are attached."
        ),
    )


def _path_effort(layer2: Layer2Result, pathway: Pathway) -> float | None:
    effort = layer2.per_path_effort.get(pathway)
    return effort.score if effort is not None else None


def _asymmetry_grade(score: float) -> LetterGrade:
    if score <= 0.15:
        return LetterGrade.A
    if score <= 0.35:
        return LetterGrade.B
    if score <= 0.60:
        return LetterGrade.C
    if score <= 0.80:
        return LetterGrade.D
    return LetterGrade.F


def _drop_grade(grade: LetterGrade) -> LetterGrade:
    index = _GRADE_ORDER.index(grade)
    return _GRADE_ORDER[min(index + 1, len(_GRADE_ORDER) - 1)]


def _first_sentence_matching(text: str, patterns: tuple[str, ...]) -> str | None:
    for sentence in _sentences(text):
        normalized = _normalize(sentence)
        if any(re.search(pattern, normalized) for pattern in patterns):
            return sentence
    return None


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [part.strip() for part in parts if part.strip()]


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _count_matches(text: str, needles: tuple[str, ...]) -> int:
    return sum(needle in text for needle in needles)


def _starts_with_benefit(text: str) -> bool:
    return bool(
        re.match(
            r"^(accept cookies|we use cookies to improve|support us|improve your experience)",
            text,
        )
    )


def _longest_sentence_word_count(text: str) -> int:
    sentence = _longest_sentence(text)
    return len(sentence.split())


def _longest_sentence(text: str) -> str:
    sentences = _sentences(text)
    if not sentences:
        return ""
    return max(sentences, key=lambda sentence: len(sentence.split()))
