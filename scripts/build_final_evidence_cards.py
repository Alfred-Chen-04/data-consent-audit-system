from __future__ import annotations

import argparse
import csv
import hashlib
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1600
HEIGHT = 1000
MARGIN = 92
FONT_PATHS = (
    Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    Path("/Library/Fonts/Arial.ttf"),
)


def _font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    paths = (
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        Path("/Library/Fonts/Arial Bold.ttf"),
    ) if bold else FONT_PATHS
    for path in paths:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def _wrap(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width, break_long_words=False) or [""]


def _draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    *,
    font: ImageFont.ImageFont,
    fill: str,
    chars: int,
    line_gap: int = 12,
) -> int:
    x, y = xy
    line_height = font.size + line_gap if hasattr(font, "size") else 36
    for line in _wrap(text, chars):
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_card(row: dict[str, str], output_dir: Path, direct_ids: set[str]) -> Path:
    source_id = row["source_id"]
    image = Image.new("RGB", (WIDTH, HEIGHT), "#F7F9FB")
    draw = ImageDraw.Draw(image)

    navy = "#101923"
    blue = "#147CB3"
    teal = "#168F82"
    gray = "#52606D"
    line = "#D4DCE3"

    draw.rectangle((0, 0, WIDTH, 150), fill=navy)
    draw.text((MARGIN, 45), source_id, font=_font(44, bold=True), fill="#62C6E6")
    lane = "DIRECT CASE SOURCE" if source_id in direct_ids else "CONTEXT / METHOD SOURCE"
    draw.text((WIDTH - 560, 58), lane, font=_font(25, bold=True), fill="white")

    y = 205
    y = _draw_wrapped(
        draw,
        row["title"],
        (MARGIN, y),
        font=_font(42, bold=True),
        fill=navy,
        chars=58,
        line_gap=10,
    )
    y += 20
    draw.text(
        (MARGIN, y),
        f'{row["publisher"]}  |  Published {row["publication_date"]}',
        font=_font(25),
        fill=gray,
    )
    y += 62
    draw.line((MARGIN, y, WIDTH - MARGIN, y), fill=line, width=3)
    y += 42

    draw.text((MARGIN, y), "SUPPORTED CLAIM", font=_font(24, bold=True), fill=teal)
    y += 42
    y = _draw_wrapped(
        draw,
        row["supports"],
        (MARGIN, y),
        font=_font(31),
        fill=navy,
        chars=82,
        line_gap=12,
    )
    y += 36

    draw.text((MARGIN, y), "SOURCE LOCATOR", font=_font(24, bold=True), fill=blue)
    y += 40
    y = _draw_wrapped(
        draw,
        row["locator"],
        (MARGIN, y),
        font=_font(27),
        fill=navy,
        chars=90,
        line_gap=10,
    )
    y += 26

    draw.text((MARGIN, y), "EVIDENCE GRADE", font=_font(24, bold=True), fill=blue)
    draw.text((MARGIN + 330, y), row["evidence_strength"], font=_font(27), fill=navy)

    draw.rectangle((MARGIN, HEIGHT - 205, WIDTH - MARGIN, HEIGHT - 72), fill="#EAF0F4")
    draw.text((MARGIN + 28, HEIGHT - 184), "OFFICIAL URL", font=_font(22, bold=True), fill=gray)
    _draw_wrapped(
        draw,
        row["url"],
        (MARGIN + 28, HEIGHT - 145),
        font=_font(22),
        fill=navy,
        chars=105,
        line_gap=7,
    )
    draw.text(
        (MARGIN, HEIGHT - 45),
        "Locator card generated 2026-08-11. It is not a reconstructed historical interface screenshot.",
        font=_font(19),
        fill=gray,
    )

    output = output_dir / f"{source_id}_source_locator_card.png"
    image.save(output, optimize=True)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry", type=Path)
    parser.add_argument("cases", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with args.cases.open(newline="", encoding="utf-8") as stream:
        case_rows = list(csv.DictReader(stream))
    direct_ids = {
        source_id
        for row in case_rows
        for source_id in row["source_ids"].split("|")
        if source_id
    }

    with args.registry.open(newline="", encoding="utf-8") as stream:
        source_rows = list(csv.DictReader(stream))

    manifest_rows: list[dict[str, str]] = []
    for row in source_rows:
        output = build_card(row, args.output_dir, direct_ids)
        manifest_rows.append(
            {
                "source_id": row["source_id"],
                "role": "direct_case_source" if row["source_id"] in direct_ids else "context_or_method_source",
                "card_path": output.as_posix(),
                "sha256": _sha256(output),
                "verified_at": "2026-08-11",
            }
        )

    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    with args.manifest.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=manifest_rows[0].keys())
        writer.writeheader()
        writer.writerows(manifest_rows)


if __name__ == "__main__":
    main()
