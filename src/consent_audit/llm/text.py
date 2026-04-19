"""LLM text calls — disclosure topic coverage, framing analysis.

Haiku for first pass; escalate to Opus on low-confidence or schema-validation failure.
"""

from consent_audit.llm.budget import BudgetLedger
from consent_audit.models import (
    DisclosureTopic,
    FramingMechanism,
    FramingResult,
    TopicCoverageResult,
)


async def classify_topics(
    banner_text: str,
    layer2_text: str | None,
    *,
    ledger: BudgetLedger,
) -> dict[DisclosureTopic, TopicCoverageResult]:
    """Per-topic presence + clarity grade + verbatim evidence quote.

    Uses function-calling / structured output so presence and quote are forced.
    """
    raise NotImplementedError("implement week 4")


async def analyze_framing(
    banner_text: str,
    layer2_text: str | None,
    *,
    ledger: BudgetLedger,
) -> dict[FramingMechanism, FramingResult]:
    """Four-channel framing analysis with evidence quotes and bias level."""
    raise NotImplementedError("implement week 4")
