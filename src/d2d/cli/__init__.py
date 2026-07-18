"""D2D command-line entry point. `d2d file.pdf` inverts to dark mode."""

import argparse
import sys

from d2d.core import (
    DEFAULT_THEME,
    THEME_INFO,
    THEMES,
    build_output_path,
    convert_file,
    get_file_extension,
    is_supported,
)

from .tui import BOLD, CORAL, DIM, GREEN, RED, banner, c, interactive_select


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Convert PDFs/images to dark mode.")
    parser.add_argument("inputs", nargs="+", help="file(s) to convert")
    parser.add_argument(
        "-t", "--theme", default=None, choices=list(THEMES),
        help=f"dark-mode theme (default: {DEFAULT_THEME}; omit for picker)",
    )
    parser.add_argument(
        "-o", "--output",
        help="output path (single input only; default inserts _dark suffix)",
    )
    args = parser.parse_args(argv)

    if args.output and len(args.inputs) > 1:
        parser.error("-o/--output cannot be used with multiple inputs")

    banner()

    theme = args.theme
    if theme is None:
        try:
            theme = interactive_select(DEFAULT_THEME)
        except KeyboardInterrupt:
            print(c("cancelled", DIM))
            return 130
    print(c("theme ", DIM) + c(THEME_INFO[theme][0], CORAL, BOLD))
    print()

    exit_code = 0
    for input_path in args.inputs:
        if not is_supported(get_file_extension(input_path)):
            print(f" {c('✗', RED)} {input_path} {c('unsupported', DIM)}")
            exit_code = 1
            continue
        output_path = args.output or build_output_path(input_path)
        try:
            convert_file(input_path, output_path, theme)
            arrow = c("→", DIM)
            print(f" {c('✓', GREEN)} {input_path} {arrow} {c(output_path, BOLD)}")
        except Exception as e:
            print(f" {c('✗', RED)} {input_path} {c(str(e), DIM)}")
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
