# Use Python slim image for smaller size
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy only what is needed for install
COPY requirements.txt .
COPY grid_overlay.py .

# Install system dependencies needed by OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run the script
ENTRYPOINT ["python", "grid_overlay.py"]
