"""Image inversion core. Depends only on PIL + numpy + the theme registry."""

import numpy as np
from PIL import Image

from .themes import DEFAULT_THEME, THEMES


def negative_trans(img: Image.Image, theme: str = DEFAULT_THEME) -> Image.Image:
    if theme not in THEMES:
        raise ValueError(f"Unknown theme: {theme}. Choose from {list(THEMES)}")
    arr = np.asarray(img.convert("RGB")).astype(np.int16)
    out = THEMES[theme](arr)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def invert_image_to_dark(input_path, output_path, theme: str = DEFAULT_THEME):
    with Image.open(input_path) as image:
        negative_img = negative_trans(image, theme)
    negative_img.save(output_path)
    return output_path
