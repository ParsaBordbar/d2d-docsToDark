import argparse
import sys
import termios
import tty

from configs import (
    DEFAULT_THEME,
    THEME_INFO,
    CORAL,
    GREEN,
    RED,
    DIM,
    BOLD,
    RESET,
    HIDE_CURSOR,
    SHOW_CURSOR,
)
from helpers import get_file_extension, is_supported_image, is_supported, build_output_path
from invertor import invert_image_to_dark, invert_pdf_to_dark, THEMES


def _color_enabled() -> bool:
    return sys.stdout.isatty()


def c(text: str, *codes: str) -> str:
    if not _color_enabled():
        return text
    return "".join(codes) + text + RESET


def banner() -> None:
    if not _color_enabled():
        return
    line = "─" * 32
    print(c(f"╭{line}╮", CORAL))
    title = f"{BOLD}D2D{RESET}{CORAL} · Docs to Dark"
    print(c("│ ", CORAL) + title + c(" " * 14 + "│", CORAL))
    print(c(f"╰{line}╯", CORAL))
    print()


def interactive_select(default: str) -> str:
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        return default

    names = list(THEMES)
    idx = names.index(default) if default in names else 0
    label_w = max(len(THEME_INFO[n][0]) for n in names)
    total_lines = len(names) + 2

    def render(first: bool) -> None:
        if not first:
            sys.stdout.write(f"\033[{total_lines}A")
        lines = [c("Select theme:", BOLD)]
        for i, name in enumerate(names):
            label, desc = THEME_INFO[name]
            if i == idx:
                pointer = c("❯ ", CORAL, BOLD)
                row = c(f"{label:<{label_w}}", CORAL, BOLD) + c(f"  {desc}", DIM)
            else:
                pointer = "  "
                row = f"{label:<{label_w}}" + c(f"  {desc}", DIM)
            lines.append(f" {pointer}{row}")
        lines.append(c("↑/↓ move · enter select · q quit", DIM))
        sys.stdout.write("".join(f"\r{ln}\033[K\r\n" for ln in lines))
        sys.stdout.flush()

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    sys.stdout.write(HIDE_CURSOR)
    try:
        tty.setraw(fd)
        first = True
        while True:
            render(first)
            first = False
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                seq = sys.stdin.read(2)
                if seq == "[A":
                    idx = (idx - 1) % len(names)
                elif seq == "[B":
                    idx = (idx + 1) % len(names)
            elif ch in ("\r", "\n"):
                break
            elif ch in ("q", "\x03"):
                raise KeyboardInterrupt
            elif ch in ("k",):
                idx = (idx - 1) % len(names)
            elif ch in ("j",):
                idx = (idx + 1) % len(names)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        sys.stdout.write(SHOW_CURSOR)
    print()
    return names[idx]


def convert(input_path: str, output_path: str, theme: str) -> str:
    ext = get_file_extension(input_path)
    if ext == ".pdf":
        return invert_pdf_to_dark(input_path, output_path, theme)
    if is_supported_image(ext):
        return invert_image_to_dark(input_path, output_path, theme)
    raise ValueError(f"Unsupported file type: {ext}")


def main(argv=None):
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
            convert(input_path, output_path, theme)
            arrow = c("→", DIM)
            print(f" {c('✓', GREEN)} {input_path} {arrow} {c(output_path, BOLD)}")
        except Exception as e:
            print(f" {c('✗', RED)} {input_path} {c(str(e), DIM)}")
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
