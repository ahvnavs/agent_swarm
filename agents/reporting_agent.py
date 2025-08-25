import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

client = OpenAI(api_key=api_key)

def generate_final_report(sales_summary: str, marketing_summary: str):
    """Synthesizes the summaries into a final report using the LLM."""
    prompt = (
        "You are a professional business analyst. Your task is to synthesize the following sales and marketing summaries "
        "into a single, comprehensive company performance report. Be sure to note any missing information from either report. "
        f"Sales Summary:\n{sales_summary}\n\n"
        f"Marketing Summary:\n{marketing_summary}\n\n"
        "Final Report:"
    )

    llm_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return llm_response.choices[0].message.content