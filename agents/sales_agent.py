import requests
import json
from transformers import pipeline # type: ignore
from typing import Any # Import Any for the type hint

# Initialize the Hugging Face summarization pipeline
try:
    # Use 'type: ignore' to tell Pylance to stop checking this line
    summarizer: Any = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6") # type: ignore
except Exception as e:
    print(f"Error loading summarization model: {e}")
    summarizer = None

def get_sales_data_and_summary() -> str:
    """
    Fetches 23 detailed sales records from the Sales API and generates
    a comprehensive Chain of Thought summary using a Hugging Face model.
    """
    if summarizer is None:
        return "Error: Hugging Face model failed to load. Cannot generate summary."

    sales_data_string = ""
    try:
        # 1. Fetch 23 detailed sales records from the API
        response = requests.get("http://sales-api:8001/sales", timeout=10)
        response.raise_for_status()
        sales_records = response.json()

        if not sales_records:
            return "No sales data found for the last 24 hours."

        # Convert the list of dictionaries into a readable string for the LLM
        sales_data_string = "Sales Records for the last 24 hours:\n"
        for i, record in enumerate(sales_records):
            sales_data_string += f"Record {i+1}: " + json.dumps(record) + "\n"
        
        # 2. Construct the Chain of Thought Prompt for the Hugging Face model
        cot_prompt = (
            "Based on the following raw sales data, provide a detailed company sales performance report. "
            "Think step-by-step to analyze the data. "
            "First, identify key metrics like total revenue, average quantity sold per transaction, and popular products/regions. "
            "Second, explain any noticeable trends or outliers. "
            "Finally, synthesize these findings into a concise, actionable summary with specific facts and figures. "
            "Here is the data:\n\n"
            f"{sales_data_string}"
        )
        
        # 3. Generate the summary using the Hugging Face pipeline
        max_summary_length = min(512, len(cot_prompt.split()) + 100)
        
        summary_result = summarizer(
            cot_prompt,
            max_length=max_summary_length,
            min_length=100,
            do_sample=False,
            truncation=True
        )
        
        return summary_result[0]['summary_text']
        
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the Sales API. Is it running? Please check network connection."
    except requests.exceptions.RequestException as e:
        return f"Error fetching sales data from API: {e}. Please ensure the API is healthy."
    except Exception as e:
        return f"Error processing sales data or generating summary: {e}. Raw data received: {sales_data_string[:500]}..."