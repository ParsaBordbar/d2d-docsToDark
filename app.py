from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import uuid

from invertor import invert_image_to_dark, invert_pdf_to_dark

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def who_am_i():
    return { "message": "Dark Mode Invertor For PDFs & Images"}

@app.post("/pdf-to-dark/")
async def invert_pdf(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.pdf")
    output_path = input_path.replace(".pdf", "_negative.pdf")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    try:
        result_path = invert_pdf_to_dark(input_path, output_path)
        return FileResponse(result_path, media_type="application/pdf", filename="negative_output.pdf")
    finally:
        pass

@app.post("/image-to-dark/")
async def invert_image(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.png")
    output_path = input_path.replace(".png", "_negative.png")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    try:
        result_path = invert_image_to_dark(input_path, output_path)
        return FileResponse(result_path, media_type="application/png", filename="negative_output.png")
    finally:
        pass
