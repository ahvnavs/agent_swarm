FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*
RUN (crontab -l 2>/dev/null; echo "0 9 * * * /usr/bin/python3 /app/main.py >> /var/log/cron.log 2>&1") | crontab -

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY startup.sh .
RUN chmod +x startup.sh

CMD ["/bin/bash", "startup.sh"]