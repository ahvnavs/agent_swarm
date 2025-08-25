from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import random
import datetime

app = FastAPI(title="Sales Mock API")

class SalesData(BaseModel):
    total_revenue: float
    new_deals_closed: int
    last_updated: str

@app.get("/sales", response_model=SalesData)
def get_sales_data() -> Dict[str, Any]:
    """
    Mock API endpoint for dynamic sales data.
    """
    # Generate random sales data
    mock_data: Dict[str, Any] = {
        "total_revenue": round(random.uniform(25000, 75000), 2),
        "new_deals_closed": random.randint(5, 25),
        "last_updated": datetime.datetime.now().isoformat()
    }
    return mock_data