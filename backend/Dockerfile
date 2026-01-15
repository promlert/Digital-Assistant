# Stage 1: Builder (ติดตั้ง dependencies)
FROM python:3.11-slim AS builder

WORKDIR /app

# ติดตั้ง dependencies ระบบที่จำเป็น (สำหรับ build บาง package)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements ก่อนเพื่อ cache layer
COPY requirements.txt .

# ติดตั้ง dependencies ใน virtual env
RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime (image สุดท้ายขนาดเล็ก)
FROM python:3.11-slim

WORKDIR /app

# Copy venv จาก builder
COPY --from=builder /venv /venv

# ติดตั้ง runtime dependencies ที่จำเป็น (เช่น สำหรับ audio/STT/TTS)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy โค้ดทั้งหมด
COPY . .

# Environment variables (สามารถ override ได้จาก docker-compose)
ENV PATH="/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Port ที่ FastAPI ใช้
EXPOSE 8000

# Command สำหรับ production (ไม่ใช้ --reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# สำหรับ development: ใช้คำสั่งนี้แทน (ใน docker-compose ใช้ command override)
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]