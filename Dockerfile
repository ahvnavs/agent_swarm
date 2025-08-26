FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir accelerate transformers torch bitsandbytes requests fpdf2 openpyxl

COPY . .

COPY startup.sh .
RUN chmod +x startup.sh

CMD ["/bin/bash", "startup.sh"]