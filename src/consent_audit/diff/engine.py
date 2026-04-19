"""Week-over-week change detection + LLM summarization.

Runs AFTER two successive AuditReports exist for the same URL.
Principle: LLM summarizes, it does NOT judge. Judgments come from Layer scores.
"""

from pydantic import HttpUrl

from consent_audit.llm.budget import BudgetLedger
from consent_audit.models import AuditReport, ChangeEvent, WeeklySummary


def detect_changes(previous: AuditReport, current: AuditReport) -> list[ChangeEvent]:
    """Compare two reports on five channels (CONCEPTS.md §5).

    Deterministic — no LLM involved.
    """
    raise NotImplementedError("implement week 7")


async def summarize_week(
    url: HttpUrl,
    events: list[ChangeEvent],
    *,
    ledger: BudgetLedger,
) -> WeeklySummary:
    """LLM authors a human-readable summary of the week's changes."""
    raise NotImplementedError("implement week 7")
