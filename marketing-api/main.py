# marketing-api/main.py
import json
import random
from fastapi import FastAPI
from datetime import date

app = FastAPI()

@app.get("/marketing")
def get_marketing_data():
    """Generates and returns a mock marketing data record."""
    today = date.today().strftime("%Y-%m-%d")
    data = {
        "date": today,
        "ad_spend": random.randint(5000, 15000),
        "impressions": random.randint(100000, 500000),
        "clicks": random.randint(5000, 25000),
        "campaign_success_rate": round(random.uniform(0.1, 0.4), 2),
        "traffic_source": random.choice(["Google Ads", "Social Media", "Email Campaigns"]),
    }
    return data

```

```text
# marketing-api/requirements.txt
fastapi==0.111.0
uvicorn[standard]==0.30.1
