"""PDF inversion. `pdf2image`/Poppler are imported lazily so that image-only
users never pay for — nor need to install — the Poppler system binary.
"""

from .invertor import negative_trans
from .themes import DEFAULT_THEME


def invert_pdf_to_dark(input_path, output_path, theme: str = DEFAULT_THEME):
    from pdf2image import convert_from_path  # lazy: requires Poppler at runtime

    try:
        pages = convert_from_path(input_path)
    except Exception as e:
        raise RuntimeError(
            f"PDF rendering failed — is Poppler installed? ({e})"
        ) from e
    neg_images = [negative_trans(page, theme) for page in pages]
    if not neg_images:
        raise ValueError("PDF has no renderable pages")
    neg_images[0].save(output_path, save_all=True, append_images=neg_images[1:])
    return output_path
