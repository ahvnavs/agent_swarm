from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import random
import datetime

app = FastAPI(title="Marketing Mock API")

class MarketingData(BaseModel):
    campaign_id: str
    campaign_name: str
    ad_spend: float
    impressions: int
    clicks: int
    conversions: int
    timestamp: str

@app.get("/marketing", response_model=MarketingData)
def get_marketing_data() -> Dict[str, Any]:
    try:
        campaign_names = ["Spring Sale", "Winter Campaign", "Holiday Ad", "Q3 Push", "Summer Offer"]

        ad_spend = round(random.uniform(500, 2000), 2)
        impressions = random.randint(10000, 50000)
        clicks = random.randint(100, 500)
        conversions = random.randint(5, 50)
        
        time_offset = datetime.timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
        transaction_time = datetime.datetime.now() - time_offset

        record: Dict[str, Any] = {
            "campaign_id": f"CAM{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100,999)}",
            "campaign_name": random.choice(campaign_names),
            "ad_spend": ad_spend,
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "timestamp": transaction_time.isoformat()
        }
        
        return record
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")