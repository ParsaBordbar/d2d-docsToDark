"""Terminal presentation for the CLI: ANSI colors, banner, theme picker.

Kept apart from argument parsing so `d2d.cli` stays about control flow.
"""

import sys
import termios
import tty

from d2d.core import DEFAULT_THEME, THEME_INFO, THEMES

CORAL = "\033[38;2;215;119;87m"
GREEN = "\033[38;2;126;186;125m"
RED = "\033[38;2;224;108;117m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


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


def interactive_select(default: str = DEFAULT_THEME) -> str:
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
