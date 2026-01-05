from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
import requests

from helpers import get_file_extension, is_supported_image
from invertor import invert_image_to_dark, invert_pdf_to_dark

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def who_am_i():
    return { "message": "Dark Mode Invertor For PDFs & Images"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    output_path = input_path.replace(".pdf", "_dark.pdf")

    with open(input_path, "wb") as f:
        f.write(await file.read())
    try:
        file_extension = get_file_extension(input_path)
        print(file_extension)
        if (file_extension == '.pdf'):
            invert_pdf_to_dark(input_path, output_path)
        elif (is_supported_image(file_extension)):
            invert_image_to_dark(input_path, output_path)
        return {"download_url": f"/download/{os.path.basename(output_path)}"}
    except:
        return {"error": "Send a valid Doc, supported ones are pdf & Images"}

@app.post("/upload-url/")
async def upload_from_url(file):
    try:
        response = requests.get(file)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download the file from the")

        file_ext = get_file_extension(file)
        if not (file_ext == '.pdf' or is_supported_image(file_ext)):
            raise ValueError("Unsupported file type")

        input_filename = f"{uuid.uuid4()}{file_ext}"
        input_path = os.path.join(UPLOAD_DIR, input_filename)
        output_path = input_path.replace(".pdf", "_dark.pdf") if file_ext == '.pdf' else input_path.replace(file_ext, f"_dark{file_ext}")

        with open(input_path, "wb") as f:
            f.write(response.content)

        if file_ext == '.pdf':
            invert_pdf_to_dark(input_path, output_path)
        else:
            invert_image_to_dark(input_path, output_path)

        return {"download": f"/download/{os.path.basename(output_path)}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename)
    return {"error": "File not found"}

