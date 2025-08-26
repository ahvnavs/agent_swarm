import os
from transformers import pipeline
from typing import Any, List, Dict
import json
import re
from .helpers import generate_pdf_report, generate_excel_file

try:
    summarizer: Any = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
except Exception as e:
    print(f"Error loading summarization model: {e}")
    summarizer = None

def generate_final_report(sales_summary: str, marketing_summary: str) -> str:
    if summarizer is None:
        return "Error: Hugging Face model failed to load. Cannot generate summary."

    tot_prompt = (
        "TASK: Create a comprehensive company performance report. "
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
        
        "5. **FINAL REPORT DRAFTING:** Combine all the analysis, trends, scenarios, and recommendations into a comprehensive report. "
        "Format the report clearly with headings for each section.\n\n"
        "--- END THINKING PROCESS ---\n\n"
        "FINAL REPORT:"
    )

    try:
        summary_result = summarizer(
            tot_prompt,
            max_length=512,
            min_length=150,
            do_sample=False,
            truncation=True
        )
        
        # Check if the result is valid before accessing the index
        if not summary_result or 'summary_text' not in summary_result[0]:
            raise Exception("Model returned an invalid or empty summary.")
        
        report_text = summary_result[0]['summary_text']

        # The rest of the file generation logic remains the same
        excel_data: List[Dict[str, Any]] = [
            {"Metric": "Total Combined Revenue", "Value": "N/A"},
            {"Metric": "Average Daily Ad Spend", "Value": "N/A"},
            {"Metric": "Average Daily Conversions", "Value": "N/A"}
        ]
        
        generate_pdf_report(report_text)
        generate_excel_file(excel_data)
        
        return report_text
    
    except Exception as e:
        # This will now catch any issues, including the index error
        return f"Error generating final report: {e}"