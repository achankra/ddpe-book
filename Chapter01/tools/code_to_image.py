#!/usr/bin/env python3
"""Small utility to render a source file to a PNG using pygments.

Usage:
    python3 tools/code_to_image.py ../01-01-abstraction.py --out=abstraction.png

Install deps: pip install pygments pillow
"""
import argparse
from pathlib import Path

from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import get_lexer_for_filename


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path, help="source file to render")
    parser.add_argument("--out", type=Path, default=Path("out.png"), help="output PNG path")
    parser.add_argument("--style", default="monokai", help="pygments style to use (monokai, default)")
    parser.add_argument("--font", default="DejaVu Sans Mono", help="font name for renderer")
    parser.add_argument("--fontsize", type=int, default=14, help="font size")
    args = parser.parse_args()

    text = args.file.read_text(encoding="utf-8")
    lexer = get_lexer_for_filename(str(args.file))
    formatter = ImageFormatter(style=args.style, font_name=args.font, font_size=args.fontsize, line_numbers=False)

    img_bytes = highlight(text, lexer, formatter)
    # ImageFormatter returns binary bytes; write to file
    args.out.write_bytes(img_bytes)
    print(f"Wrote image to {args.out}")


if __name__ == "__main__":
    main()
