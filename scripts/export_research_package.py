"""Export all paper-facing research tables plus a small manifest."""
# ruff: noqa: E402

import sys
from pathlib import Path

import typer

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts._bootstrap import ensure_src_on_path

ensure_src_on_path()

from consent_audit.research_package import export_research_package

app = typer.Typer()


@app.command()
def main(
    out_dir: Path = Path("data/research_package"),
    limit: int = 500,
) -> None:
    manifest = _run(out_dir, limit=limit)
    typer.echo(
        "Wrote research package "
        f"({manifest['audit_report_count']} reports, "
        f"{manifest['weekly_summary_count']} weekly summaries) to {out_dir}"
    )


def _run(out_dir: Path, *, limit: int = 500) -> dict[str, object]:
    return export_research_package(out_dir, limit=limit)


if __name__ == "__main__":
    app()
