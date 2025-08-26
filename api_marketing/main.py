from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
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

@app.get("/marketing", response_model=List[MarketingData])
def get_marketing_data() -> List[Dict[str, Any]]:
    try:
        marketing_records: List[Dict[str, Any]] = []
        campaign_names = ["Spring Sale", "Winter Campaign", "Holiday Ad", "Q3 Push", "Summer Offer"]
        for i in range(23):
            ad_spend = round(random.uniform(500, 2000), 2)
            impressions = random.randint(10000, 50000)
            clicks = random.randint(100, 500)
            conversions = random.randint(5, 50)
            time_offset = datetime.timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
            transaction_time = datetime.datetime.now() - time_offset
            record: Dict[str, Any] = {
                "campaign_id": f"CAM{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{i:02d}{random.randint(100,999)}",
                "campaign_name": random.choice(campaign_names),
                "ad_spend": ad_spend,
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "timestamp": transaction_time.isoformat()
            }
            marketing_records.append(record)
        return marketing_records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")