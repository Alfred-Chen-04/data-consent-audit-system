"""Weekly pipeline: audit every site in the list, diff against last week, store summaries.

Scheduled via APScheduler or an OS-level cron. On failure for a single site, continue
the rest — log the failure, do not abort the run (AGENTS.md §7 — budget cap is the
only hard abort condition).
"""
# ruff: noqa: E402

import asyncio
import sys
from pathlib import Path

import typer

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts._bootstrap import ensure_src_on_path

ensure_src_on_path()

from consent_audit.pipeline import (
    WeeklyRunSummary,
    audit_weekly_site,
    format_weekly_run_summary,
    load_site_urls,
    run_weekly_audit,
)

app = typer.Typer()


@app.command()
def main(
    sites_csv: Path = Path("data/sites.csv"),
    consent_table_path: Path | None = Path("data/consent_table.csv"),
    cohort: str = "weekly",
    limit: int | None = None,
) -> None:
    try:
        summary = asyncio.run(
            _run(
                sites_csv,
                consent_table_path=consent_table_path,
                cohort=cohort,
                limit=limit,
            )
        )
    except ValueError as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    typer.echo(format_weekly_run_summary(summary))


async def _run(
    sites_csv: Path,
    *,
    consent_table_path: Path | None = None,
    cohort: str = "weekly",
    limit: int | None = None,
) -> WeeklyRunSummary:
    return await run_weekly_audit(
        sites_csv,
        consent_table_path=consent_table_path,
        cohort=cohort,
        limit=limit,
    )


_audit_one = audit_weekly_site
_load_urls = load_site_urls


if __name__ == "__main__":
    app()
