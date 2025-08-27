# Use a lightweight official Python image
FROM python:3.10-slim

# Install system dependencies for cron and PDF generation
RUN apt-get update && apt-get install -y cron libgirepository1.0-dev libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the application files
COPY . .

# Create the log file for cron
RUN touch /var/log/cron.log

# Create a cron job file
RUN echo "0 9 * * * python3 /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/daily_report_cron

# Give execute permissions to the cron job file
RUN chmod 0644 /etc/cron.d/daily_report_cron

# Apply the cron job
RUN crontab /etc/cron.d/daily_report_cron

# Run the cron service in the foreground.
# We also use tail to keep the container running indefinitely.
CMD ["cron", "-f"]