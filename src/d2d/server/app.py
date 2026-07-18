import asyncio
import os
import time
import uuid
from contextlib import asynccontextmanager
from functools import partial

import requests
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from d2d.core import (
    DEFAULT_THEME,
    THEMES,
    build_output_path,
    convert_file,
    get_file_extension,
    is_supported,
)

from .config import (
    ALLOWED_ORIGINS,
    APP_INFO,
    APP_TITLE,
    CLEANUP_INTERVAL_SECONDS,
    DOWNLOAD_TIMEOUT_SECONDS,
    FILE_MAX_AGE_SECONDS,
    UPLOAD_DIR,
)

os.makedirs(UPLOAD_DIR, exist_ok=True)


def cleanup_old_files():
    now = time.time()
    for name in os.listdir(UPLOAD_DIR):
        path = os.path.join(UPLOAD_DIR, name)
        try:
            if os.path.isfile(path) and now - os.path.getmtime(path) > FILE_MAX_AGE_SECONDS:
                os.remove(path)
        except OSError:
            pass


async def _cleanup_loop():
    while True:
        cleanup_old_files()
        await asyncio.sleep(CLEANUP_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(_cleanup_loop())
    yield
    task.cancel()


app = FastAPI(title=APP_TITLE, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _resolve_theme(theme: str | None) -> str:
    if theme is None:
        return DEFAULT_THEME
    if theme not in THEMES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown theme '{theme}'. Choose from {list(THEMES)}",
        )
    return theme


def _convert(input_path: str, theme: str = DEFAULT_THEME) -> str:
    output_path = build_output_path(input_path)
    return convert_file(input_path, output_path, theme)


async def _save_upload(file: UploadFile) -> str:
    input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    with open(input_path, "wb") as f:
        f.write(await file.read())
    return input_path


@app.get("/")
async def who_am_i():
    return APP_INFO


@app.get("/themes")
async def list_themes():
    return {"themes": list(THEMES), "default": DEFAULT_THEME}


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), theme: str = Form(None)):
    theme = _resolve_theme(theme)
    input_path = await _save_upload(file)
    try:
        output_path = await run_in_threadpool(_convert, input_path, theme)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process file: {e}")
    return {"download_url": f"/download/{os.path.basename(output_path)}"}


@app.post("/batch/")
async def upload_batch(files: list[UploadFile] = File(...), theme: str = Form(None)):
    theme = _resolve_theme(theme)
    results = []
    for file in files:
        input_path = await _save_upload(file)
        try:
            output_path = await run_in_threadpool(_convert, input_path, theme)
            results.append({
                "filename": file.filename,
                "download_url": f"/download/{os.path.basename(output_path)}",
            })
        except Exception as e:
            results.append({"filename": file.filename, "error": str(e)})
    return {"results": results}


@app.post("/upload-url/")
async def upload_from_url(file: str, theme: str = None):
    theme = _resolve_theme(theme)
    file_ext = get_file_extension(file)
    if not is_supported(file_ext):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        response = await run_in_threadpool(partial(requests.get, file, timeout=DOWNLOAD_TIMEOUT_SECONDS))
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to download the file: {e}")
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download the file from the URL")

    input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{file_ext}")
    with open(input_path, "wb") as f:
        f.write(response.content)

    try:
        output_path = await run_in_threadpool(_convert, input_path, theme)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")
    return {"download_url": f"/download/{os.path.basename(output_path)}"}


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")
