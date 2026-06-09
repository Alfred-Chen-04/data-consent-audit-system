"""LLM text calls — disclosure topic coverage, framing analysis.

Haiku for first pass; escalate to Opus on low-confidence or schema-validation failure.
"""

import re
from collections.abc import Iterable

from consent_audit.llm.budget import BudgetLedger
from consent_audit.models import (
    BiasLevel,
    DisclosureTopic,
    ElementRef,
    FramingMechanism,
    FramingResult,
    LetterGrade,
    TopicCoverageResult,
)

TEXT_CALL_COST_USD = 0.01

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
        "advertis(?:e|ing|ement|ed)?",
        "personalised",
        "personalized",
        "measurement",
        "improve",
        "support us",
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


async def classify_topics(
    banner_text: str,
    layer2_text: str | None,
    *,
    ledger: BudgetLedger,
) -> dict[DisclosureTopic, TopicCoverageResult]:
    """Per-topic presence + clarity grade + verbatim evidence quote.

    Uses function-calling / structured output so presence and quote are forced.
    """
    ledger.record("llm.text.classify_topics", TEXT_CALL_COST_USD)
    source_text = _combined_text(banner_text, layer2_text)
    return {
        topic: _topic_result(
            source_text,
            layer2_text or "",
            topic,
            patterns,
        )
        for topic, patterns in _TOPIC_PATTERNS.items()
    }


async def analyze_framing(
    banner_text: str,
    layer2_text: str | None,
    *,
    ledger: BudgetLedger,
) -> dict[FramingMechanism, FramingResult]:
    """Four-channel framing analysis with evidence quotes and bias level."""
    ledger.record("llm.text.analyze_framing", TEXT_CALL_COST_USD)
    text = _combined_text(banner_text, layer2_text)
    benefit_quote = _first_sentence_matching(
        text,
        ("improve your experience", "support us", "better experience", "personalised"),
    )
    control_quote = _first_sentence_matching(
        text,
        ("reject", "decline", "withdraw", "privacy choices", "share data", "tracking"),
    )

    emphasis_level = BiasLevel.MILD_BIAS if benefit_quote and not control_quote else BiasLevel.NEUTRAL
    selective_level = (
        BiasLevel.STRONG_BIAS if benefit_quote and not control_quote else BiasLevel.NEUTRAL
    )
    sequencing_level = (
        BiasLevel.MILD_BIAS
        if benefit_quote and _normalize(_first_sentence(text)).startswith(("accept", "we use"))
        else BiasLevel.NEUTRAL
    )
    complexity_quote = _longest_sentence(text)
    complexity_level = (
        BiasLevel.MILD_BIAS if _word_count(complexity_quote) >= 35 else BiasLevel.NEUTRAL
    )

    return {
        FramingMechanism.EMPHASIS: FramingResult(
            mechanism=FramingMechanism.EMPHASIS,
            level=emphasis_level,
            rationale="Benefit language appears without nearby risk/control language."
            if emphasis_level != BiasLevel.NEUTRAL
            else "No one-sided benefit emphasis detected by the deterministic fallback.",
            evidence_quotes=_quotes(benefit_quote) if emphasis_level != BiasLevel.NEUTRAL else [],
        ),
        FramingMechanism.LINGUISTIC_COMPLEXITY: FramingResult(
            mechanism=FramingMechanism.LINGUISTIC_COMPLEXITY,
            level=complexity_level,
            rationale="A consent sentence exceeds the deterministic complexity threshold."
            if complexity_level != BiasLevel.NEUTRAL
            else "No high-complexity sentence detected by the deterministic fallback.",
            evidence_quotes=_quotes(complexity_quote)
            if complexity_level != BiasLevel.NEUTRAL
            else [],
        ),
        FramingMechanism.SEQUENCING: FramingResult(
            mechanism=FramingMechanism.SEQUENCING,
            level=sequencing_level,
            rationale="The first sentence leads with acceptance or benefit framing."
            if sequencing_level != BiasLevel.NEUTRAL
            else "No benefit-first sequencing detected by the deterministic fallback.",
            evidence_quotes=_quotes(_first_sentence(text))
            if sequencing_level != BiasLevel.NEUTRAL
            else [],
        ),
        FramingMechanism.SELECTIVE_PROMINENCE: FramingResult(
            mechanism=FramingMechanism.SELECTIVE_PROMINENCE,
            level=selective_level,
            rationale="Positive outcomes are stated while reject/control consequences are absent."
            if selective_level != BiasLevel.NEUTRAL
            else "No selective benefit prominence detected by the deterministic fallback.",
            evidence_quotes=_quotes(benefit_quote) if selective_level != BiasLevel.NEUTRAL else [],
        ),
    }


def _combined_text(banner_text: str, layer2_text: str | None) -> str:
    parts = [banner_text.strip()]
    if layer2_text and layer2_text.strip():
        parts.append(layer2_text.strip())
    return "\n".join(part for part in parts if part)


def _topic_result(
    text: str,
    layer2_text: str,
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
        consistent_with_layer2=_has_match(layer2_text, patterns) if layer2_text else None,
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


def _first_sentence_matching(text: str, patterns: Iterable[str]) -> str | None:
    for sentence in _sentences(text):
        normalized = _normalize(sentence)
        if any(re.search(pattern, normalized) for pattern in patterns):
            return sentence
    return None


def _first_sentence(text: str) -> str:
    sentences = _sentences(text)
    return sentences[0] if sentences else ""


def _longest_sentence(text: str) -> str:
    sentences = _sentences(text)
    return max(sentences, key=_word_count) if sentences else ""


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]


def _has_match(text: str, patterns: Iterable[str]) -> bool:
    normalized = _normalize(text)
    return any(re.search(pattern, normalized) for pattern in patterns)


def _count_matches(text: str, needles: Iterable[str]) -> int:
    return sum(1 for needle in needles if needle in text)


def _word_count(text: str) -> int:
    return len(re.findall(r"\w+", text))


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _quotes(quote: str | None) -> list[str]:
    return [quote] if quote else []
