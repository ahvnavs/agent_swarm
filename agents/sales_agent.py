import os
import requests
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

client = OpenAI(api_key=api_key)

def get_sales_data_and_summary():
    """Fetches sales data and generates a summary using the LLM."""
    try:
        response = requests.get("http://sales-api:8001/sales")
        response.raise_for_status()
        sales_data = json.dumps(response.json())
        
        prompt = (
            "You are an expert sales data analyst. Analyze the following sales data and provide a concise, structured summary. "
            "Data: " + sales_data
        )
        
        llm_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return llm_response.choices[0].message.content
        
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the Sales API. Is it running?"
    except requests.exceptions.RequestException as e:
        return f"Error fetching sales data: {e}"