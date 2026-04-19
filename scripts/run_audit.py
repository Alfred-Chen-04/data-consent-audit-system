"""Audit a single URL. Thin wrapper around the library.

Usage:
    uv run python scripts/run_audit.py --url https://example.com
"""

import asyncio

import typer

from consent_audit.capture import capture_site
from consent_audit.config import settings
from consent_audit.layers import score_layer1, score_layer2, score_layer3
from consent_audit.llm.budget import BudgetLedger
from consent_audit.report import generate_report
from consent_audit.storage import save_report

app = typer.Typer()


@app.command()
def main(url: str, save: bool = True) -> None:
    asyncio.run(_run(url, save=save))


async def _run(url: str, *, save: bool) -> None:
    ledger = BudgetLedger(cap_usd=settings.ssrp_budget_cap)

    bundle = await capture_site(url, timeout_seconds=settings.agent_site_timeout)  # type: ignore[arg-type]
    l1 = score_layer1(bundle)

    l2 = score_layer2(bundle, l1) if l1.gate_passed else None
    l3 = score_layer3(bundle, l1, l2) if l2 is not None else None

    report = generate_report(bundle, l1, l2, l3, api_cost_usd=ledger.spent_usd)

    if save:
        save_report(report)
    typer.echo(report.report_markdown)


if __name__ == "__main__":
    app()
