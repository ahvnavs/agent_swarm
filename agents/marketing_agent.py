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

def get_marketing_data_and_summary() -> str:
    """
    Fetches 23 detailed marketing records from the Marketing API and generates
    a comprehensive Chain of Thought summary using a Hugging Face model.
    """
    if summarizer is None:
        return "Error: Hugging Face model failed to load. Cannot generate summary."
        
    marketing_data_string = ""
    try:
        # 1. Fetch 23 detailed marketing records from the API
        response = requests.get("http://marketing-api:8002/marketing", timeout=10) # Added a timeout for robustness
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        marketing_records = response.json() # This will be a list of dictionaries

        if not marketing_records:
            return "No marketing data found for the last 24 hours."

        # Convert the list of dictionaries into a readable string for the LLM
        marketing_data_string = "Marketing Records for the last 24 hours:\n"
        for i, record in enumerate(marketing_records):
            marketing_data_string += f"Record {i+1}: " + json.dumps(record) + "\n"
        
        # 2. Construct the Chain of Thought Prompt for the Hugging Face model
        cot_prompt = (
            "Based on the following raw marketing data, provide a detailed company marketing performance report. "
            "Think step-by-step to analyze the data. "
            "First, identify key metrics like total ad spend, average clicks and impressions per campaign, and conversion rates. "
            "Second, explain any noticeable trends or outliers. "
            "Finally, synthesize these findings into a concise, actionable summary with specific facts and figures. "
            "Here is the data:\n\n"
            f"{marketing_data_string}"
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
        return "Error: Could not connect to the Marketing API. Is it running? Please check network connection."
    except requests.exceptions.RequestException as e:
        return f"Error fetching marketing data from API: {e}. Please ensure the API is healthy."
    except Exception as e:
        return f"Error processing marketing data or generating summary: {e}. Raw data received: {marketing_data_string[:500]}..."