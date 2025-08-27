import json
import random
from fastapi import FastAPI
from datetime import date

app = FastAPI()

@app.get("/sales")
def get_sales_data():
    """Generates and returns a mock sales data record."""
    today = date.today().strftime("%Y-%m-%d")
    data = {
        "date": today,
        "total_revenue": random.randint(50000, 150000),
        "new_customers": random.randint(50, 200),
        "top_product_id": random.choice(["PROD_A", "PROD_B", "PROD_C"]),
        "conversion_rate_percent": round(random.uniform(2.5, 7.5), 2),
    }
    return data