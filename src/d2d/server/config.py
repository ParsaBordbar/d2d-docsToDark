"""Server-only runtime configuration, all env-overridable."""

import os

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

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
