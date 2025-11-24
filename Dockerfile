# ===============================
# 1) Base Image
# ===============================
FROM python:3.11-slim AS base

# Prevent Python from writing .pyc files and using stdout buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ===============================
# 2) Working Directory
# ===============================
WORKDIR /app

# ===============================
# 3) Install System Dependencies
# ===============================
# (Required for psycopg2, pillow, numpy, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# 4) Install Python Dependencies
# ===============================
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# 5) Copy Application Code
# ===============================
COPY . .

# ===============================
# 6) Expose & Run Server
# ===============================
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
