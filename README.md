# Docs To Dark (D2D)
<img width="1470" height="956" alt="image" src="https://github.com/user-attachments/assets/443bfb88-7f81-4f5a-a7e6-799afb3e1778" />

Transform your PDFs and images into dark mode with a simple API! No more disconfort for your eyes when studying!

## What is D2D?

D2D (Docs to Dark) is a FastAPI-based web service that inverts the colors of PDFs and images, converting them to dark mode. Perfect for reading documents at night or reducing eye strain!

## ✨ Features

- 📄 **PDF Support**: Convert entire PDF documents to dark mode
- 🖼️ **Image Support**: PNG, JPG, JPEG, BMP, WEBP, TIFF, and GIF formats
- 🎨 **Themes**: Pick how darkness looks — `hue` (color-preserving), `invert` (classic), `dim`, `sepia`, `midnight`
- 🚀 **Fast Processing**: Built on FastAPI; blocking conversion runs in a threadpool so the server stays responsive
- 📤 **Multiple Upload Options**: Upload single files, batches, or via URL
- 🖥️ **CLI**: Convert from the terminal with an interactive theme picker — no server needed
- 🧹 **Auto Cleanup**: Background scheduler removes old files automatically
- 💾 **Easy Downloads**: Get your converted files instantly

## 🎨 Themes

Every conversion takes an optional `theme` (default: `hue`). Pure inversion turns colored content into its complement (red → cyan); `hue` instead inverts only lightness, so colors stay recognizable in dark mode.

| Theme | What it does |
|-------|--------------|
| `hue` | Inverts lightness, preserves hue/saturation (default) |
| `invert` | Classic negative, maximum contrast |
| `dim` | Softer blacks/whites, easier on the eyes |
| `sepia` | Warm-toned dark background |
| `midnight` | Cool blue-tinted dark |

`GET /themes` returns the live list and the default.

## Prerequisites

- Python 3.10 or higher (required by `numpy`)
- pip or [uv](https://docs.astral.sh/uv/) (Python package manager)
- Poppler (for PDF processing)

### Installing Poppler

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
Download from [poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/) and add to PATH.

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/D2D.git
cd D2D
```

2. **Set up the environment and install dependencies:**

Using **uv** (fast, recommended):
```bash
cd server
uv venv
uv pip install -r requirements.txt
```
With `uv`, prefix run commands with `uv run` and skip manual activation.

Or classic **venv + pip**:
```bash
cd server
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> Dependencies (including `numpy`, used for the theme transforms) are pinned in `server/requirements.txt`. Poppler must still be installed system-wide (see above).

## Running the Application

Start the server with:

```bash
cd server
uvicorn app:app --reload --host 0.0.0.0 --port 1313
```

The API will be available at `http://localhost:1313`

### Or run with docker-compose!

```bash
cd server
docker compose up --build
```

## 🖥️ Command-line (no server)

Convert files straight from the terminal. Runs the same conversion engine as the API.

```bash
cd server
python cli.py document.pdf            # interactive theme picker (↑/↓, enter)
python cli.py photo.jpg -t sepia      # pick a theme, skip the picker
python cli.py photo.png -o out.png    # choose the output path
python cli.py *.png --theme dim       # batch convert
```

With `uv`: `uv run python cli.py document.pdf`.

When no `-t/--theme` is given and you're in a real terminal, an interactive picker appears (arrow keys or `j`/`k`, `enter` to select, `q` to quit). Piped/non-interactive runs fall back to the default theme. Output files get a `_dark` suffix unless `-o` is set.

## Frontend (client)

A React + Vite UI lives in `client/`. It supports drag-and-drop, multi-file upload, URL upload, and a theme selector that applies to the next conversion.

```bash
cd client
npm install
npm run dev
```

The client reads the API base URL from `VITE_API_BASE_URL` (`client/.env`, defaults to `http://localhost:1313`).

### Configuration (server env vars)

| Variable | Default | Purpose |
|----------|---------|---------|
| `ALLOWED_ORIGINS` | `*` | Comma-separated CORS origins |
| `CLEANUP_INTERVAL_SECONDS` | `900` | How often the cleanup scheduler runs |
| `FILE_MAX_AGE_SECONDS` | `3600` | Age after which uploaded/converted files are deleted |

## 📖 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: `http://localhost:1313/docs`
- **Alternative Docs**: `http://localhost:1313/redoc`

Supported formats: **PDF**, and images **PNG, JPG, JPEG, BMP, WEBP, TIFF, GIF**.

## 🔌 API Endpoints

### 1. Root Endpoint
```
GET /
```
Returns service information.

### Themes
```
GET /themes
```
Returns the available themes and the default:
```json
{ "themes": ["invert", "hue", "dim", "sepia", "midnight"], "default": "hue" }
```

### 2. Upload File
```
POST /upload/
```
Upload a single PDF or image file for conversion. Optional `theme` form field (default `hue`); an unknown theme returns `400`.

**Example using curl:**
```bash
curl -X POST "http://localhost:1313/upload/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf" \
  -F "theme=sepia"
```

**Response:**
```json
{
  "download_url": "/download/filename_dark.pdf"
}
```

### 3. Batch Upload
```
POST /batch/
```
Convert multiple files in one request. Returns a per-file result list (each item is a success with `download_url` or an `error`). Optional `theme` form field applies to all files.

**Example using curl:**
```bash
curl -X POST "http://localhost:1313/batch/" \
  -F "files=@/path/to/a.pdf" \
  -F "files=@/path/to/b.png" \
  -F "theme=midnight"
```

**Response:**
```json
{
  "results": [
    { "filename": "a.pdf", "download_url": "/download/..._dark.pdf" },
    { "filename": "b.png", "download_url": "/download/..._dark.png" }
  ]
}
```

### 4. Upload from URL
```
POST /upload-url/?file=<url>&theme=<theme>
```
Provide a URL (as the `file` query parameter) to a PDF or image for conversion. Optional `theme` query parameter (default `hue`).

**Example:**
```bash
curl -X POST "http://localhost:1313/upload-url/?file=https://example.com/document.pdf&theme=dim"
```

### 5. Download File
```
GET /download/{filename}
```
Download your converted dark mode file.

**Example:**
```bash
curl -O "http://localhost:1313/download/filename_dark.pdf"
```

## Usage Example

**Python Example:**
```python
import requests

# Upload a file
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:1313/upload/', files=files)
    download_url = response.json()['download_url']

# Download the converted file
converted = requests.get(f'http://localhost:1313{download_url}')
with open('document_dark.pdf', 'wb') as f:
    f.write(converted.content)
```

**JavaScript/Node.js Example:**
```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('document.pdf'));

axios.post('http://localhost:1313/upload/', form, {
    headers: form.getHeaders()
})
.then(response => {
    console.log('Download URL:', response.data.download_url);
})
.catch(error => {
    console.error('Error:', error);
});
```

## Project Structure

```
D2D/
├── server/                 # FastAPI backend
│   ├── app.py              # routes + orchestration
│   ├── invertor.py         # image/PDF processing + theme registry
│   ├── helpers.py          # extension/mime helpers
│   ├── cli.py              # terminal version (interactive theme picker)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── uploads/            # ephemeral, auto-cleaned (gitignored)
└── client/                 # React + Vite + Tailwind frontend
    └── src/
        ├── components/Uploader/   # drag-and-drop UI + theme selector
        ├── hooks/useUpload.ts     # upload state + conversion
        └── api/upload.ts          # network layer
```

## Notes To Consider 

- Uploaded files are stored temporarily in the `uploads/` directory
- A background scheduler deletes files older than `FILE_MAX_AGE_SECONDS` (default 1 hour); tune via env vars
- Large PDFs may take longer to process
- Ensure adequate disk space for temporary file storage

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Troubleshooting

**Issue: "Poppler not found"**
- Make sure Poppler is installed and accessible in your system PATH

**Issue: "Module not found"**
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**Issue: "Permission denied on uploads/"**
- Check folder permissions: `chmod 755 uploads/`

## 💡 Future Enhancements

- [x] Batch processing support
- [x] Support for more file formats
- [x] File cleanup scheduler
- [x] Theme presets (hue-preserving, sepia, dim, midnight)
- [x] Command-line interface
- [ ] Adjustable brightness/contrast knobs
- [ ] Async jobs + progress for very large PDFs
- [ ] Preview before download

## Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ for flow students and readers! Have fun!
