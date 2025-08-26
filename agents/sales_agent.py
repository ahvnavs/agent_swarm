import os # type: ignore
import requests # type: ignore
import json
from transformers import pipeline # type: ignore
from typing import Any

try:
    summarizer: Any = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6") # type: ignore
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
        sales_records = response.json()
        print("SALES AGENT RECEIVED DATA:", sales_records)
        if not sales_records:
            return "No sales data found for the last 24 hours."
        sales_data_string = "Sales Records for the last 24 hours:\n"
        for i, record in enumerate(sales_records):
            sales_data_string += f"Record {i+1}: " + json.dumps(record) + "\n"
        cot_prompt = (
            "Based on the following raw sales data, provide a detailed company sales performance report. "
            "Think step-by-step to analyze the data. "
            "First, identify key metrics like total revenue, average quantity sold per transaction, and popular products/regions. "
            "Second, explain any noticeable trends or outliers. "
            "Finally, synthesize these findings into a concise, actionable summary with specific facts and figures. "
            "Here is the data:\n\n"
            f"{sales_data_string}"
        )
        max_summary_length = min(512, len(cot_prompt.split()) + 100)
        summary_result = summarizer(
            cot_prompt,
            max_length=max_summary_length,
            min_length=100,
            do_sample=False,
            truncation=True
        )
        if summary_result and 'summary_text' in summary_result[0]:
            return summary_result[0]['summary_text']
        else:
            return "Error: Could not generate a valid summary from the model."
        
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the Sales API. Is it running? Please check network connection."
    except requests.exceptions.RequestException as e:
        return f"Error fetching sales data from API: {e}. Please ensure the API is healthy."
    except Exception as e:
        return f"Error processing sales data or generating summary: {e}. Raw data received: {sales_data_string[:500]}..."