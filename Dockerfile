# Use latest Python
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install supervisor to manage multiple processes
RUN pip install supervisor

# Expose Streamlit (8501) + Flask (8000)
EXPOSE 8501 8000

# Use supervisord to run both
CMD ["supervisord", "-c", "/app/supervisord.conf"]
