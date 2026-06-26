import os

UPLOAD_DIR = "uploads"

CLEANUP_INTERVAL_SECONDS = int(os.getenv("CLEANUP_INTERVAL_SECONDS", 900))
FILE_MAX_AGE_SECONDS = int(os.getenv("FILE_MAX_AGE_SECONDS", 3600))

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

DOWNLOAD_TIMEOUT_SECONDS = int(os.getenv("DOWNLOAD_TIMEOUT_SECONDS", 30))

APP_TITLE = "D2D - Docs to Dark"

APP_INFO = {
    "name": "Docs To Dark (D2D)",
    "tagline": "Transform your PDFs and images into dark mode",
    "description": "Dark Mode Invertor For PDFs & Images",
    "docs": "/docs",
}

SUPPORTED_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff", ".tif", ".gif"]
PDF_EXTENSION = ".pdf"

DEFAULT_THEME = "hue"

THEME_INFO = {
    "hue": ("Hue-preserving", "invert lightness, keep colors natural"),
    "invert": ("Pure invert", "classic negative, max contrast"),
    "dim": ("Dim", "softer blacks/whites, easy on the eyes"),
    "sepia": ("Sepia", "warm-toned dark background"),
    "midnight": ("Midnight", "cool blue-tinted dark"),
}

CORAL = "\033[38;2;215;119;87m"
GREEN = "\033[38;2;126;186;125m"
RED = "\033[38;2;224;108;117m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
