# Use a more complete base image that includes cron
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install cron and add the cron job
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*
RUN (crontab -l 2>/dev/null; echo "0 9 * * * /usr/bin/python3 /app/main.py >> /var/log/cron.log 2>&1") | crontab -

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install new libraries for PDF and Excel generation
RUN pip install --no-cache-dir fpdf2 openpyxl

# Copy all the application files
COPY . .

# Run the startup script
COPY startup.sh .
RUN chmod +x startup.sh

# Run the startup script
CMD ["/bin/bash", "startup.sh"]