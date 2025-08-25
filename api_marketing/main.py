from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="Marketing Mock API")

# A Pydantic model to define the structure of the data we'll return
class MarketingData(BaseModel):
    ad_spend: float
    ctr_percent: float
    conversions: int
    last_updated: str

@app.get("/marketing", response_model=MarketingData)
def get_marketing_data() -> Dict[str, Any]:
    """
    Mock API endpoint for marketing data.
    """
    # This is our hardcoded, mock data.
    mock_data: Dict[str, Any] = {
        "ad_spend": 1200.50,
        "ctr_percent": 2.5,
        "conversions": 80,
        "last_updated": "2025-08-26T09:05:00Z"
    }
    return mock_data