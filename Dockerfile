# TinyTots Tunes - AI Preschool YouTube Video Factory Docker Container
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Install system dependencies including FFmpeg, fonts, and graphics libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    fonts-comic-neue \
    fonts-dejavu-core \
    libsm6 \
    libxext6 \
    libgl1 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app

# Ensure writable directories for projects, data, and output
RUN mkdir -p /app/data /app/projects /app/output /app/temp

# Expose HTTP port
EXPOSE 8000

# Start FastAPI dashboard and automation worker
CMD ["sh", "-c", "uvicorn dashboard.app:app --host 0.0.0.0 --port ${PORT:-8000}"]
