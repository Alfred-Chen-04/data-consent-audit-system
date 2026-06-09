"""Tests for deterministic text-analysis LLM wrapper fallbacks."""

import pytest

from consent_audit.llm.budget import BudgetExceeded, BudgetLedger
from consent_audit.llm.text import analyze_framing, classify_topics
from consent_audit.models import DisclosureTopic, FramingMechanism, LetterGrade


@pytest.mark.asyncio
async def test_classify_topics_records_budget_and_uses_verbatim_quotes() -> None:
    ledger = BudgetLedger(cap_usd=1.0)
    banner_text = (
        "We use cookies and device identifiers for analytics and personalized ads. "
        "We share data with advertising partners. "
        "You can accept, reject, or customize these choices."
    )

    result = await classify_topics(banner_text, None, ledger=ledger)

    assert ledger.entries == [("llm.text.classify_topics", 0.01)]
    assert result[DisclosureTopic.DATA_TYPES].present
    assert result[DisclosureTopic.DATA_TYPES].clarity_grade in {
        LetterGrade.A,
        LetterGrade.B,
    }
    for topic_result in result.values():
        if topic_result.evidence_quote is not None:
            assert topic_result.evidence_quote in banner_text


@pytest.mark.asyncio
async def test_analyze_framing_records_budget_and_uses_source_quotes() -> None:
    ledger = BudgetLedger(cap_usd=1.0)
    banner_text = "Accept cookies to improve your experience and support us."

    result = await analyze_framing(banner_text, None, ledger=ledger)

    assert ledger.entries == [("llm.text.analyze_framing", 0.01)]
    selective = result[FramingMechanism.SELECTIVE_PROMINENCE]
    assert selective.evidence_quotes == [banner_text]
    assert selective.evidence_quotes[0] in banner_text


@pytest.mark.asyncio
async def test_text_wrappers_fail_cleanly_when_budget_cap_is_exceeded() -> None:
    ledger = BudgetLedger(cap_usd=0.0)

    with pytest.raises(BudgetExceeded):
        await classify_topics("We use cookies.", None, ledger=ledger)

    assert ledger.spent_usd == 0.0
    assert ledger.entries == []
