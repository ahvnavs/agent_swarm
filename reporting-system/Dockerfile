FROM python:3.10-slim

RUN apt-get update && apt-get install -y cron libgirepository1.0-dev libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN touch /var/log/cron.log

RUN echo "0 9 * * * python3 /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/daily_report_cron

RUN chmod 0644 /etc/cron.d/daily_report_cron

RUN crontab /etc/cron.d/daily_report_cron

CMD ["cron", "-f"]