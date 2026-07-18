"""D2D conversion core — pure, dependency-light, shared by CLI and server."""

from .helpers import (
    PDF_EXTENSION,
    SUPPORTED_IMAGE_EXTENSIONS,
    build_output_path,
    get_file_extension,
    get_mime_type,
    is_supported,
    is_supported_image,
)
from .invertor import invert_image_to_dark, negative_trans
from .pdf import invert_pdf_to_dark
from .themes import DEFAULT_THEME, THEME_INFO, THEMES


def convert_file(input_path, output_path, theme: str = DEFAULT_THEME):
    """Dispatch a single file to the right inverter by extension.

    Shared by the CLI and the server so dispatch logic lives in exactly one place.
    """
    ext = get_file_extension(input_path)
    if ext == PDF_EXTENSION:
        return invert_pdf_to_dark(input_path, output_path, theme)
    if is_supported_image(ext):
        return invert_image_to_dark(input_path, output_path, theme)
    raise ValueError(f"Unsupported file type: {ext}")


__all__ = [
    "SUPPORTED_IMAGE_EXTENSIONS",
    "PDF_EXTENSION",
    "DEFAULT_THEME",
    "THEME_INFO",
    "THEMES",
    "get_file_extension",
    "get_mime_type",
    "is_supported",
    "is_supported_image",
    "build_output_path",
    "negative_trans",
    "invert_image_to_dark",
    "invert_pdf_to_dark",
    "convert_file",
]
