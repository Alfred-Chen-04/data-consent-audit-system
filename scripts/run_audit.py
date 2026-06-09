"""Audit a single URL. Thin wrapper around the library.

Usage:
    uv run python scripts/run_audit.py --url https://example.com
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

from consent_audit.pipeline import run_single_site_audit

app = typer.Typer()


@app.command()
def main(
    url: str,
    save: bool = True,
    consent_table_path: Path | None = Path("data/consent_table.csv"),
    cohort: str = "",
) -> None:
    asyncio.run(_run(url, save=save, consent_table_path=consent_table_path, cohort=cohort))


async def _run(
    url: str,
    *,
    save: bool,
    consent_table_path: Path | None = None,
    cohort: str = "",
) -> None:
    report = await run_single_site_audit(
        url,
        save=save,
        consent_table_path=consent_table_path,
        cohort=cohort,
    )
    typer.echo(report.report_markdown)


if __name__ == "__main__":
    app()
