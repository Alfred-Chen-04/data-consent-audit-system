"""Tests for API budget enforcement."""

from consent_audit.llm.budget import BudgetExceeded, BudgetLedger


def test_budget_ledger_records_spend_under_cap() -> None:
    ledger = BudgetLedger(cap_usd=1.0)

    ledger.record("vision", 0.25)

    assert ledger.spent_usd == 0.25
    assert ledger.entries == [("vision", 0.25)]


def test_budget_ledger_raises_before_exceeding_cap() -> None:
    ledger = BudgetLedger(cap_usd=0.5, spent_usd=0.4)

    try:
        ledger.record("text", 0.2)
    except BudgetExceeded:
        pass
    else:  # pragma: no cover - kept explicit for direct no-pytest harnesses
        raise AssertionError("BudgetExceeded was not raised")

    assert ledger.spent_usd == 0.4
    assert ledger.entries == []
