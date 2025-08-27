import requests
import os
from huggingface_hub import InferenceClient

class MarketingAgent:
    """
    An agent to fetch marketing data and generate a summary using Hugging Face Inference API.
    """
    def __init__(self):
        self.api_url = "http://marketing-api:8000/marketing"
        self.api_key = os.environ.get("LLM_API_KEY")
        self.client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2", token=self.api_key)

    def get_summary(self):
        """Fetches marketing data and generates a summary."""
        if not self.api_key:
            return "Error: LLM_API_KEY environment variable not set."

        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            marketing_data = response.json()
            
            prompt_data = (
                f"You are a marketing analyst. Based on the following data, "
                f"provide a concise summary of today's key marketing campaign metrics.\n\n"
                f"Data: {marketing_data}\n\n"
                f"Summary:"
            )
            
            summary_response = self.client.text_generation(prompt_data, max_new_tokens=256)
            
            summary = summary_response.replace(prompt_data, "").strip()
            
            return summary
            
        except requests.exceptions.RequestException as e:
            return f"Error: Could not retrieve data from marketing API. Details: {e}"
        except Exception as e:
            return f"Error: An unexpected error occurred in MarketingAgent. Details: {e}"