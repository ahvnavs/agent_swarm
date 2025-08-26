import os
import requests
import json
from transformers import pipeline
from typing import Any

try:
    # Use the flan-t5-base model for better instruction following
    summarizer: Any = pipeline("text2text-generation", model="google/flan-t5-base")
except Exception as e:
    print(f"Error loading summarization model: {e}")
    summarizer = None

def get_sales_data_and_summary() -> str:
    if summarizer is None:
        return "Error: Hugging Face model failed to load. Cannot generate summary."
    sales_data_string = ""
    try:
        response = requests.get("http://sales-api:8001/sales", timeout=10)
        response.raise_for_status()
        sales_record = response.json()
        
        if not sales_record:
            return "No sales data found for the last 24 hours."
            
        sales_data_string = json.dumps(sales_record)
        
        # New, more detailed prompt
        prompt = (
            "Based on the following sales data, provide a detailed summary of the sales performance, "
            "highlighting the product, revenue, and customer region. "
            "Analyze and explain the key performance indicators.\n\n"
            "Sales Data:\n"
            f"{sales_data_string}"
        )
        
        # Flan-T5 has a different output format, so we get the text directly
        summary_result = summarizer(prompt)
        
        if summary_result and 'generated_text' in summary_result[0]:
            return summary_result[0]['generated_text']
        else:
            return "Error: Could not generate a valid summary from the model."
    
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the Sales API. Is it running? Please check network connection."
    except requests.exceptions.RequestException as e:
        return f"Error fetching sales data from API: {e}. Please ensure the API is healthy."
    except Exception as e:
        return f"Error processing sales data or generating summary: {e}. Raw data received: {sales_data_string[:500]}..."