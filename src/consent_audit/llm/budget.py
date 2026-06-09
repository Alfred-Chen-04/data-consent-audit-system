"""Cumulative API-cost tracking. Every LLM / VLM call must go through here.

See AGENTS.md §7 — budget cap is enforced per run; exceeding aborts the pipeline.
"""

from dataclasses import dataclass, field


class BudgetExceededError(Exception):
    """Raised when cumulative spend would exceed the configured cap."""


@dataclass
class BudgetLedger:
    cap_usd: float
    spent_usd: float = 0.0
    entries: list[tuple[str, float]] = field(default_factory=list)

    def record(self, label: str, cost_usd: float) -> None:
        if self.spent_usd + cost_usd > self.cap_usd:
            raise BudgetExceededError(
                f"{label}: adding ${cost_usd:.4f} would exceed cap ${self.cap_usd:.2f}"
            )
        self.spent_usd += cost_usd
        self.entries.append((label, cost_usd))


BudgetExceeded = BudgetExceededError
