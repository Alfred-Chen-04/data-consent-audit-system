from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfReader, PdfWriter, Transformation

POINTS_PER_INCH = 72


def _fit_page(source: Path, output: Path, width_inches: int, height_inches: int) -> None:
    reader = PdfReader(source)
    if len(reader.pages) != 1:
        raise ValueError("Expected a one-page poster PDF")

    source_page = reader.pages[0]
    source_width = float(source_page.mediabox.width)
    source_height = float(source_page.mediabox.height)
    target_width = width_inches * POINTS_PER_INCH
    target_height = height_inches * POINTS_PER_INCH
    scale = min(target_width / source_width, target_height / source_height)
    translate_x = (target_width - source_width * scale) / 2
    translate_y = (target_height - source_height * scale) / 2

    writer = PdfWriter()
    target_page = writer.add_blank_page(width=target_width, height=target_height)
    target_page.merge_transformed_page(
        source_page,
        Transformation().scale(scale).translate(translate_x, translate_y),
    )
    writer.add_metadata(
        {
            "/Title": f"How Cookie Consent Interfaces Changed - {width_inches}x{height_inches}",
            "/Author": "Qianyi (Alfred) Chen",
            "/Subject": "CWRU Intersections print-ready research poster",
        }
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as stream:
        writer.write(stream)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("small", type=Path)
    parser.add_argument("large", type=Path)
    args = parser.parse_args()

    _fit_page(args.source, args.small, width_inches=40, height_inches=32)
    _fit_page(args.source, args.large, width_inches=60, height_inches=40)


if __name__ == "__main__":
    main()
