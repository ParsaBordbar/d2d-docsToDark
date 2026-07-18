"""Extension / mime detection and output-path building. No heavy deps."""

import mimetypes
import os

SUPPORTED_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff", ".tif", ".gif"]
PDF_EXTENSION = ".pdf"


def get_file_extension(file_path: str) -> str:
    return os.path.splitext(file_path)[1].lower()


def is_supported_image(extension: str) -> bool:
    return extension.lower() in SUPPORTED_IMAGE_EXTENSIONS


def is_supported(extension: str) -> bool:
    return extension.lower() == PDF_EXTENSION or is_supported_image(extension)


def build_output_path(input_path: str) -> str:
    root, ext = os.path.splitext(input_path)
    return f"{root}_dark{ext.lower()}"


def get_mime_type(file_path: str):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type
