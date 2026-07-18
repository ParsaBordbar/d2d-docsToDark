"""Dark-mode theme registry: numpy transforms + human-facing metadata.

Pure numerical code — no PIL, FastAPI, or CLI deps. This is the single source
of truth for what themes exist; both the CLI and the server import from here.
"""

import numpy as np

DEFAULT_THEME = "hue"

# name -> (label, description) shown in the CLI picker and /themes endpoint
THEME_INFO = {
    "hue": ("Hue-preserving", "invert lightness, keep colors natural"),
    "invert": ("Pure invert", "classic negative, max contrast"),
    "dim": ("Dim", "softer blacks/whites, easy on the eyes"),
    "sepia": ("Sepia", "warm-toned dark background"),
    "midnight": ("Midnight", "cool blue-tinted dark"),
}


def _pure_invert(arr: np.ndarray) -> np.ndarray:
    return 255 - arr


def _hue_invert(arr: np.ndarray) -> np.ndarray:
    mx = arr.max(axis=2, keepdims=True)
    mn = arr.min(axis=2, keepdims=True)
    return arr + (255 - mx - mn)


def _dim(arr: np.ndarray) -> np.ndarray:
    base = np.clip(_hue_invert(arr), 0, 255)
    return base * ((230 - 24) / 255.0) + 24


def _sepia(arr: np.ndarray) -> np.ndarray:
    base = np.clip(_hue_invert(arr), 0, 255).astype(np.float32)
    base[..., 0] *= 1.07
    base[..., 2] *= 0.82
    return base


def _midnight(arr: np.ndarray) -> np.ndarray:
    base = np.clip(_hue_invert(arr), 0, 255).astype(np.float32)
    base[..., 0] *= 0.88
    base[..., 2] *= 1.10
    return base


THEMES = {
    "invert": _pure_invert,
    "hue": _hue_invert,
    "dim": _dim,
    "sepia": _sepia,
    "midnight": _midnight,
}
