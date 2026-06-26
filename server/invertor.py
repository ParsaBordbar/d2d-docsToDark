import numpy as np
from PIL import Image
from pdf2image import convert_from_path

from configs import DEFAULT_THEME


def _pure_invert(arr: np.ndarray) -> np.ndarray:
    return 255 - arr


def _hue_invert(arr: np.ndarray) -> np.ndarray:
    mx = arr.max(axis=2, keepdims=True)
    mn = arr.min(axis=2, keepdims=True)
    return arr + (255 - mx - mn)


def _dim(arr: np.ndarray) -> np.ndarray:
    base = _hue_invert(arr)
    base = np.clip(base, 0, 255)
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


def negative_trans(img: Image.Image, theme: str = DEFAULT_THEME) -> Image.Image:
    if theme not in THEMES:
        raise ValueError(f"Unknown theme: {theme}. Choose from {list(THEMES)}")
    arr = np.asarray(img.convert("RGB")).astype(np.int16)
    out = THEMES[theme](arr)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def invert_pdf_to_dark(input_path, output_path, theme: str = DEFAULT_THEME):
    pages = convert_from_path(input_path)
    neg_images = [negative_trans(page, theme) for page in pages]
    if not neg_images:
        raise ValueError("PDF has no renderable pages")
    neg_images[0].save(output_path, save_all=True, append_images=neg_images[1:])
    return output_path


def invert_image_to_dark(input_path, output_path, theme: str = DEFAULT_THEME):
    with Image.open(input_path) as image:
        negative_img = negative_trans(image, theme)
    negative_img.save(output_path)
    return output_path
