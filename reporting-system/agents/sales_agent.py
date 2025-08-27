import requests
import os
from groq import Groq

class SalesAgent:
    """
    An agent to fetch sales data and generate a summary using Groq's LLM API.
    """
    def __init__(self):
        self.api_url = "http://sales-api:8000/sales"
        self.api_key = os.environ.get("LLM_API_KEY")

        # Explicitly remove proxy environment variables before client initialization.
        # This fixes the "unexpected keyword argument 'proxies'" error.
        if "http_proxy" in os.environ:
            del os.environ["http_proxy"]
        if "https_proxy" in os.environ:
            del os.environ["https_proxy"]

        self.client = Groq(api_key=self.api_key)
        self.model_name = "mixtral-8x7b-32768"

    def get_summary(self):
        """Fetches sales data and generates a summary."""
        if not self.api_key:
            return "Error: LLM_API_KEY environment variable not set."

        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            sales_data = response.json()

            messages = [
                {
                    "role": "system",
                    "content": "You are a business analyst. Provide a concise summary of today's key sales metrics."
                },
                {
                    "role": "user",
                    "content": f"Data: {sales_data}"
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

        except requests.exceptions.RequestException as e:
            return f"Error: Could not retrieve data from sales API. Details: {e}"
        except Exception as e:
            return f"Error: An unexpected error occurred in SalesAgent. Details: {e}"