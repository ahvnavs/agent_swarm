import os
from transformers import pipeline
from typing import Any
import json
import re
from helpers import generate_pdf_report, generate_excel_file # Import helper functions

# Initialize the Hugging Face summarization pipeline
try:
    summarizer: Any = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6") # type: ignore
except Exception as e:
    print(f"Error loading summarization model: {e}")
    summarizer = None

def generate_final_report(sales_summary: str, marketing_summary: str) -> str:
    """
    Synthesizes summaries into a multi-page report using a Tree of Thoughts (ToT) approach
    and generates a PDF and Excel file.
    """
    if summarizer is None:
        return "Error: Hugging Face model failed to load. Cannot generate summary."

    # Step 1: Simulate a Tree of Thoughts (ToT)
    # The ToT approach guides the model to explore multiple paths of reasoning
    # This is done through a structured, multi-step prompt.
    tot_prompt = (
        "TASK: Create a 23-page comprehensive company performance report. "
        "The report must contain detailed numbers, facts, and figures from the sales and marketing summaries. "
        "Include a current scenario analysis, strategic suggestions, and specific cost-cutting recommendations.\n\n"
        "Raw Sales Summary:\n" + sales_summary + "\n\n"
        "Raw Marketing Summary:\n" + marketing_summary + "\n\n"
        "--- START THINKING PROCESS (Tree of Thoughts) ---\n\n"
        
        "1. **CORE ANALYSIS:** Identify the most critical metrics and trends from both summaries. "
        "Calculate key performance indicators (KPIs) like total combined revenue, ad spend-to-revenue ratio, and conversion rates.\n\n"
        
        "2. **TREND IDENTIFICATION:** Look for positive and negative trends. Are sales increasing or decreasing? "
        "Are marketing campaigns becoming more or less effective? Identify any clear anomalies or outliers.\n\n"
        
        "3. **STRATEGIC SCENARIOS:** Based on the trends, propose three different scenarios for the company's future performance. "
        "For each scenario, detail the potential outcome.\n\n"
        
        "4. **ACTIONABLE RECOMMENDATIONS:** For each scenario, provide specific, numbered recommendations. "
        "Focus on cost-cutting measures for underperforming areas and investment suggestions for high-performing areas.\n\n"
        
        "5. **FINAL REPORT DRAFTING:** Combine all the analysis, trends, scenarios, and recommendations into a comprehensive, multi-page report draft. "
        "Format the report clearly with headings for each section. "
        "The report must be at least 23 pages long, so be incredibly detailed with all your analysis.\n\n"
        "--- END THINKING PROCESS ---\n\n"
        "FINAL REPORT:"
    )

    try:
        # Generate the detailed report using the ToT prompt
        report_text = summarizer(
            tot_prompt,
            max_length=4096,  # Use a large max_length for a detailed report
            min_length=1500,  # Min length to enforce detail
            do_sample=False,
            truncation=True
        )[0]['summary_text']
        
        # Step 2: Extract key numbers and metrics for the Excel file
        # This is a simplified example; a more complex regex could be used
        excel_data = [
            {"Metric": "Total Combined Revenue", "Value": "N/A"},
            {"Metric": "Average Daily Ad Spend", "Value": "N/A"},
            {"Metric": "Average Daily Conversions", "Value": "N/A"}
        ]
        
        # You would use regex or a more robust parsing method here
        # to extract the numbers from report_text
        
        # Step 3: Generate the PDF and Excel files
        generate_pdf_report(report_text)
        generate_excel_file(excel_data)
        
        return report_text
        
    except Exception as e:
        return f"Error generating final report: {e}"