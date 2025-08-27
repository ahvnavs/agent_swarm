import requests
import os
from huggingface_hub import InferenceClient

class SalesAgent:
    """
    An agent to fetch sales data and generate a summary using Hugging Face Inference API.
    """
    def __init__(self):
        self.api_url = "http://sales-api:8000/sales"
        self.api_key = os.environ.get("LLM_API_KEY")
        # Initialize the Inference Client with the API key and model name
        self.client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2", token=self.api_key)

    def get_summary(self):
        """Fetches sales data and generates a summary."""
        if not self.api_key:
            return "Error: LLM_API_KEY environment variable not set."

        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            sales_data = response.json()
            
            prompt_data = (
                f"You are a business analyst. Based on the following data, "
                f"provide a concise summary of today's key sales metrics.\n\n"
                f"Data: {sales_data}\n\n"
                f"Summary:"
            )
            
            # Use the client to perform text generation
            summary_response = self.client.text_generation(prompt_data, max_new_tokens=256)
            
            # The API's response will include the prompt, so we remove it.
            summary = summary_response.replace(prompt_data, "").strip()
            
            return summary
            
        except requests.exceptions.RequestException as e:
            return f"Error: Could not retrieve data from sales API. Details: {e}"
        except Exception as e:
            return f"Error: An unexpected error occurred in SalesAgent. Details: {e}"