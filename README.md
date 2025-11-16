# D2D - Docs to Dark

Transform your PDFs and images into dark mode with a simple API! No more disconfort for your eyes when studying!

## What is D2D?

D2D (Docs to Dark) is a FastAPI-based web service that inverts the colors of PDFs and images, converting them to dark mode. Perfect for reading documents at night or reducing eye strain!

## ✨ Features

- 📄 **PDF Support**: Convert entire PDF documents to dark mode
- 🖼️ **Image Support**: Supports PNG, JPG, JPEG, and BMP formats
- 🚀 **Fast Processing**: Built on FastAPI for optimal performance
- 📤 **Multiple Upload Options**: Upload files directly or via URL
- 💾 **Easy Downloads**: Get your converted files instantly

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
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

2. **Create a virtual environment:**
```bash
python -m venv venv
```

3. **Activate the virtual environment:**

*Linux/macOS:*
```bash
source venv/bin/activate
```

*Windows:*
```bash
venv\Scripts\activate
```

4. **Install dependencies:**
```bash
pip install fastapi uvicorn pillow pdf2image python-multipart requests
```

## Running the Application

Start the server with:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

## 🔌 API Endpoints

### 1. Root Endpoint
```
GET /
```
Returns service information.

### 2. Upload File
```
POST /upload/
```
Upload a PDF or image file for conversion.

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/upload/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf"
```

**Response:**
```json
{
  "download_url": "/download/filename_dark.pdf"
}
```

### 3. Upload from URL
```
POST /upload-url/
```
Provide a URL to a PDF or image for conversion.

**Example:**
```bash
curl -X POST "http://localhost:8000/upload-url/" \
  -H "Content-Type: application/json" \
  -d '"https://example.com/document.pdf"'
```

### 4. Download File
```
GET /download/{filename}
```
Download your converted dark mode file.

**Example:**
```bash
curl -O "http://localhost:8000/download/filename_dark.pdf"
```

## Usage Example

**Python Example:**
```python
import requests

# Upload a file
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/upload/', files=files)
    download_url = response.json()['download_url']

# Download the converted file
converted = requests.get(f'http://localhost:8000{download_url}')
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

axios.post('http://localhost:8000/upload/', form, {
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
ctx3 print                               
┌── 📂 Project structure:
├── .gitignore (36 bytes)
├── app.py (2556 bytes)
├── helpers.py (399 bytes)
├── invertor.py (959 bytes)
├── requirements.txt (1550 bytes)
├── uploads (4096 bytes)
```

## Notes To Consider 

- Uploaded files are stored temporarily in the `uploads/` directory
- Consider implementing cleanup mechanisms for production use
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

- [ ] Docker support
- [ ] Batch processing support
- [ ] Support for more file formats
- [ ] File cleanup scheduler

## Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ for flow students and readers! Have fun!
