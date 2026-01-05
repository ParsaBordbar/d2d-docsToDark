FROM python:3.11-slim

WORKDIR /app


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir fastapi uvicorn pillow pdf2image python-multipart requests

COPY app.py .
COPY invertor.py .
COPY helpers.py .

RUN mkdir -p uploads

EXPOSE 1313

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "1313"]