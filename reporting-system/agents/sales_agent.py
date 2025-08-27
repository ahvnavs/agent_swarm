import requests
import os
from transformers import pipeline

class SalesAgent:
    """
    An agent to fetch sales data and generate a summary.
    """
    def __init__(self):
        # We'll use a mock LLM call since we can't run the actual model.
        # This function simulates the behavior of the Mixtral 8x7B pipeline.
        # A real implementation would download and load the model.
        # e.g., self.llm = pipeline("text-generation", model="mistralai/Mixtral-8x7B-Instruct-v0.1")
        self.llm = self.mock_llm_pipeline
        self.api_url = "http://sales-api:8000/sales"

    def mock_llm_pipeline(self, prompt, **kwargs):
        """Simulates an LLM response."""
        return [{
            "generated_text": (
                f"Sales Summary: Total revenue for the day was ${prompt['total_revenue']:,} "
                f"from {prompt['new_customers']} new customers. The conversion rate "
                f"was {prompt['conversion_rate_percent']}%, with top product ID "
                f"{prompt['top_product_id']} leading the sales."
            )
        }]

    def get_summary(self):
        """Fetches sales data and generates a summary."""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            sales_data = response.json()
            
            # The prompt for the instruction-following model
            prompt = {
                "total_revenue": sales_data.get("total_revenue"),
                "new_customers": sales_data.get("new_customers"),
                "conversion_rate_percent": sales_data.get("conversion_rate_percent"),
                "top_product_id": sales_data.get("top_product_id")
            }
            
            # Generate the summary using the LLM
            llm_response = self.llm(prompt)
            summary = llm_response[0]["generated_text"]
            
            return summary
        except requests.exceptions.RequestException as e:
            return f"Error: Could not retrieve data from sales API. Details: {e}"
        except Exception as e:
            return f"Error: An unexpected error occurred in SalesAgent. Details: {e}"