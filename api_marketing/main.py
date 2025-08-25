from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import random
import datetime

app = FastAPI(title="Marketing Mock API")

class MarketingData(BaseModel):
    ad_spend: float
    ctr_percent: float
    conversions: int
    last_updated: str

@app.get("/marketing", response_model=MarketingData)
def get_marketing_data() -> Dict[str, Any]:
    """
    Mock API endpoint for dynamic marketing data.
    """
    # Generate random marketing data
    mock_data: Dict[str, Any] = {
        "ad_spend": round(random.uniform(800, 1500), 2),
        "ctr_percent": round(random.uniform(1.5, 5.0), 2),
        "conversions": random.randint(50, 100),
        "last_updated": datetime.datetime.now().isoformat()
    }
    return mock_data