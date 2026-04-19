"""Command-line interface. `uv run consent-audit --help` once installed."""

import typer
from rich import print as rprint

app = typer.Typer(help="Dynamic consent interface audit system.")


@app.command()
def audit(url: str, output: str = "report.md") -> None:
    """Audit a single URL and write a Markdown report."""
    rprint(f"[yellow]Stub[/yellow] — would audit {url} → {output}")
    raise typer.Exit(code=1)


@app.command()
def weekly(sites_csv: str = "data/sites.csv") -> None:
    """Run the full weekly pipeline against a CSV of URLs."""
    rprint(f"[yellow]Stub[/yellow] — would run weekly pipeline over {sites_csv}")
    raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
