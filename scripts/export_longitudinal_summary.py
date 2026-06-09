"""Export saved WeeklySummary rows to a paper-facing CSV."""
# ruff: noqa: E402

import sys
from pathlib import Path

import typer

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts._bootstrap import ensure_src_on_path

ensure_src_on_path()

from consent_audit.longitudinal_export import export_weekly_summaries_to_csv
from consent_audit.storage import list_weekly_summaries

app = typer.Typer()


@app.command()
def main(
    out_csv: Path = Path("data/longitudinal_summary.csv"),
    limit: int = 500,
) -> None:
    _run(out_csv, limit=limit)


def _run(out_csv: Path, *, limit: int = 500) -> None:
    summaries = list_weekly_summaries(limit=limit)
    export_weekly_summaries_to_csv(out_csv, summaries)
    typer.echo(f"Wrote {len(summaries)} weekly summaries to {out_csv}")


if __name__ == "__main__":
    app()
