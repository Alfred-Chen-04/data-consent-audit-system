"""Export saved AuditReport rows to a paper-facing CSV."""
# ruff: noqa: E402

import sys
from pathlib import Path

import typer

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts._bootstrap import ensure_src_on_path

ensure_src_on_path()

from consent_audit.audit_export import export_audit_reports_to_csv
from consent_audit.storage import list_reports

app = typer.Typer()


@app.command()
def main(
    out_csv: Path = Path("data/audit_report_summary.csv"),
    limit: int = 500,
) -> None:
    _run(out_csv, limit=limit)


def _run(out_csv: Path, *, limit: int = 500) -> None:
    reports = list_reports(limit=limit)
    export_audit_reports_to_csv(out_csv, reports)
    typer.echo(f"Wrote {len(reports)} audit reports to {out_csv}")


if __name__ == "__main__":
    app()
