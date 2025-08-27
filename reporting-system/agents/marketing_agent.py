import requests
import os
from groq import Groq
import httpx # Import httpx library

class MarketingAgent:
    """
    An agent to fetch marketing data and generate a summary using Groq's LLM API.
    """
    def __init__(self):
        self.api_url = "http://marketing-api:8000/marketing"
        self.api_key = os.environ.get("LLM_API_KEY")

        if "http_proxy" in os.environ:
            del os.environ["http_proxy"]
        if "https_proxy" in os.environ:
            del os.environ["https_proxy"]

        http_client = httpx.Client(proxies={})
        self.client = Groq(api_key=self.api_key, http_client=http_client)
        self.model_name = "llama3-8b-8192"

    def get_data(self):
        """Fetches raw data from the marketing API."""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: Could not retrieve data from marketing API. Details: {e}"
        except Exception as e:
            return f"Error: An unexpected error occurred in MarketingAgent. Details: {e}"
    
    def get_summary(self, marketing_data):
        """Generates a summary from the provided marketing data."""
        if not self.api_key:
            return "Error: LLM_API_KEY environment variable not set."
        if isinstance(marketing_data, str) and marketing_data.startswith("Error:"):
            return marketing_data
            
        try:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a senior marketing analyst for a B2B SaaS company. "
                        "Your task is to provide a comprehensive, industry-standard summary of daily marketing campaign performance. "
                        "The summary should be detailed and structured with bullet points. "
                        "Include an analysis of total ad spend, impressions, clicks, campaign success rate, "
                        "and top traffic sources. Conclude with an overall sentiment on the day's marketing efforts."
                    )
                },
                {
                    "role": "user",
                    "content": f"Today's Marketing Data: {marketing_data}"
                }
            ]
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                temperature=0.7,
                max_tokens=256
            )
            
            summary = chat_completion.choices[0].message.content.strip()
            return summary
        except Exception as e:
            return f"Error: An unexpected error occurred in MarketingAgent. Details: {e}"