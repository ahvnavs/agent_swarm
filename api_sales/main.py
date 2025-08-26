from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List, Dict, Any
import random
import datetime

app = FastAPI(title="Sales Mock API") # type: ignore
class SalesData(BaseModel): # type: ignore
    transaction_id: str
    product_name: str
    quantity_sold: int
    unit_price: float
    total_revenue: float
    customer_region: str
    timestamp: str

@app.get("/sales", response_model=List[SalesData]) # type: ignore
def get_sales_data() -> List[Dict[str, Any]]:
    try:
        sales_records: List[Dict[str, Any]] = []
        product_names = ["Laptop", "Mouse", "Keyboard", "Monitor", "Webcam", "Headphones", "Microphone"]
        customer_regions = ["North", "South", "East", "West", "Central"]
        for i in range(23):
            unit_price = round(random.uniform(50, 1500), 2)
            quantity_sold = random.randint(1, 10)
            total_revenue = round(unit_price * quantity_sold, 2)
            time_offset = datetime.timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
            transaction_time = datetime.datetime.now() - time_offset
            record: Dict[str, Any] = {
                "transaction_id": f"TRX{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{i:02d}{random.randint(100,999)}",
                "product_name": random.choice(product_names),
                "quantity_sold": quantity_sold,
                "unit_price": unit_price,
                "total_revenue": total_revenue,
                "customer_region": random.choice(customer_regions),
                "timestamp": transaction_time.isoformat()
            }
            sales_records.append(record)
        return sales_records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")