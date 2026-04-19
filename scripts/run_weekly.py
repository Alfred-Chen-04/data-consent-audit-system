"""Weekly pipeline: audit every site in the list, diff against last week, store summaries.

Scheduled via APScheduler or an OS-level cron. On failure for a single site, continue
the rest — log the failure, do not abort the run (AGENTS.md §7 — budget cap is the
only hard abort condition).
"""

import asyncio
import csv
from pathlib import Path

import structlog
import typer

from consent_audit.capture import capture_site
from consent_audit.config import settings
from consent_audit.diff import detect_changes, summarize_week
from consent_audit.layers import score_layer1, score_layer2, score_layer3
from consent_audit.llm.budget import BudgetExceeded, BudgetLedger
from consent_audit.report import generate_report
from consent_audit.storage import list_reports_for_url, save_report

log = structlog.get_logger()
app = typer.Typer()


@app.command()
def main(sites_csv: Path = Path("data/sites.csv")) -> None:
    asyncio.run(_run(sites_csv))


async def _run(sites_csv: Path) -> None:
    ledger = BudgetLedger(cap_usd=settings.ssrp_budget_cap)

    with sites_csv.open() as fh:
        urls = [row["url"] for row in csv.DictReader(fh)]

    for url in urls:
        try:
            await _audit_one(url, ledger)
        except BudgetExceeded:
            log.error("budget_exceeded", url=url, spent=ledger.spent_usd)
            break
        except Exception as exc:
            log.error("site_failed", url=url, error=str(exc))
            continue


async def _audit_one(url: str, ledger: BudgetLedger) -> None:
    bundle = await capture_site(url, timeout_seconds=settings.agent_site_timeout)  # type: ignore[arg-type]
    l1 = score_layer1(bundle)
    l2 = score_layer2(bundle, l1) if l1.gate_passed else None
    l3 = score_layer3(bundle, l1, l2) if l2 is not None else None
    report = generate_report(bundle, l1, l2, l3, api_cost_usd=ledger.spent_usd)
    save_report(report)

    history = list_reports_for_url(url, limit=2)  # type: ignore[arg-type]
    if len(history) >= 2:
        events = detect_changes(history[1], history[0])
        if events:
            await summarize_week(url, events, ledger=ledger)  # type: ignore[arg-type]


if __name__ == "__main__":
    app()
