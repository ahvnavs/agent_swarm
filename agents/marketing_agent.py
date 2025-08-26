import os
import requests
import json
from transformers import pipeline
from typing import Any

try:
    summarizer: Any = pipeline("text2text-generation", model="google/flan-t5-base")
except Exception as e:
    print(f"Error loading summarization model: {e}")
    summarizer = None

def get_marketing_data_and_summary() -> str:
    if summarizer is None:
        return "Error: Hugging Face model failed to load. Cannot generate summary."
    marketing_data_string = ""
    try:
        response = requests.get("http://marketing-api:8002/marketing", timeout=10)
        response.raise_for_status()
        marketing_record = response.json()
        
        if not marketing_record:
            return "No marketing data found for the last 24 hours."
            
        marketing_data_string = json.dumps(marketing_record)
        
        prompt = (
            "Based on the following marketing data, provide a detailed summary of the campaign's performance, "
            "highlighting ad spend, impressions, clicks, and conversions. "
            "Analyze and explain the key performance indicators.\n\n"
            "Marketing Data:\n"
            f"{marketing_data_string}"
        )
        
        summary_result = summarizer(prompt)
        
        if summary_result and 'generated_text' in summary_result[0]:
            return summary_result[0]['generated_text']
        else:
            return "Error: Could not generate a valid summary from the model."
    
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the Marketing API. Is it running? Please check network connection."
    except requests.exceptions.RequestException as e:
        return f"Error fetching marketing data from API: {e}. Please ensure the API is healthy."
    except Exception as e:
        return f"Error processing marketing data or generating summary: {e}. Raw data received: {marketing_data_string[:500]}..."