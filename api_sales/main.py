from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="Sales Mock API")

# A Pydantic model to define the structure of the data we'll return
class SalesData(BaseModel):
    total_revenue: float
    new_deals_closed: int
    last_updated: str

@app.get("/sales", response_model=SalesData)
def get_sales_data() -> Dict[str, Any]:
    """
    Mock API endpoint for sales data.
    """
    # This is our hardcoded, mock data.
    mock_data: Dict[str, Any] = {
        "total_revenue": 50000.75,
        "new_deals_closed": 15,
        "last_updated": "2025-08-26T09:00:00Z"
    }
    return mock_data