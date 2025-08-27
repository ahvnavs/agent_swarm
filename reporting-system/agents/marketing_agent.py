import requests
import os
from transformers import pipeline

class MarketingAgent:
    """
    An agent to fetch marketing data and generate a summary.
    """
    def __init__(self):
        # We'll use a mock LLM call since we can't run the actual model.
        self.llm = self.mock_llm_pipeline
        self.api_url = "http://marketing-api:8000/marketing"

    def mock_llm_pipeline(self, prompt, **kwargs):
        """Simulates an LLM response."""
        return [{
            "generated_text": (
                f"Marketing Summary: Ad spend for the day was ${prompt['ad_spend']:,} "
                f"resulting in {prompt['impressions']:,} impressions and {prompt['clicks']:,} clicks. "
                f"The most successful traffic source was {prompt['traffic_source']} "
                f"with a campaign success rate of {prompt['campaign_success_rate']}."
            )
        }]

    def get_summary(self):
        """Fetches marketing data and generates a summary."""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            marketing_data = response.json()
            
            prompt = {
                "ad_spend": marketing_data.get("ad_spend"),
                "impressions": marketing_data.get("impressions"),
                "clicks": marketing_data.get("clicks"),
                "traffic_source": marketing_data.get("traffic_source"),
                "campaign_success_rate": marketing_data.get("campaign_success_rate")
            }
            
            llm_response = self.llm(prompt)
            summary = llm_response[0]["generated_text"]
            
            return summary
        except requests.exceptions.RequestException as e:
            return f"Error: Could not retrieve data from marketing API. Details: {e}"
        except Exception as e:
            return f"Error: An unexpected error occurred in MarketingAgent. Details: {e}"