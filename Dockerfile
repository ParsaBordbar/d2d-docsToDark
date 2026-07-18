FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    poppler-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install the package with the server extra from source.
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir ".[server]"

RUN mkdir -p uploads

EXPOSE 1313

CMD ["uvicorn", "d2d.server.app:app", "--host", "0.0.0.0", "--port", "1313"]
