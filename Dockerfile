# Use a complete base image
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3-pip \
    cron \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Install all Python dependencies in one single step to prevent caching issues
RUN pip install --no-cache-dir \
    accelerate \
    transformers \
    torch \
    bitsandbytes \
    requests \
    fpdf2 \
    openpyxl \
    python-dotenv

# Copy all the application files
COPY . .

# Set up cron job
RUN (crontab -l 2>/dev/null; echo "0 9 * * * /usr/bin/python /app/main.py >> /var/log/cron.log 2>&1") | crontab -

# Run the startup script
COPY startup.sh .
RUN chmod +x startup.sh
CMD ["/bin/bash", "startup.sh"]