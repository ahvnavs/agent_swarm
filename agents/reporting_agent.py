import os
from transformers import pipeline
from typing import Any, List, Dict
import json
import re
from .helpers import generate_pdf_report, generate_excel_file

try:
    # Use the flan-t5-base model for better instruction following
    model_name = "google/flan-t5-base"
    flan_t5_generator: Any = pipeline("text2text-generation", model=model_name)
except Exception as e:
    print(f"Error loading model: {e}")
    flan_t5_generator = None

def generate_final_report(sales_summary: str, marketing_summary: str) -> str:
    if flan_t5_generator is None:
        return "Error: Model failed to load. Cannot generate summary."

    # Step 1: Generate a detailed report body
    report_prompt = (
        "Based on the following sales and marketing data summaries, create a comprehensive company performance report. "
        "The report must include a detailed analysis of key metrics, observed trends, a summary of current scenarios, "
        "and actionable recommendations for improvement, including cost-cutting measures. "
        "Use facts and figures from the provided summaries to support your analysis. "
        "Summaries:\n\n"
        "Sales Summary:\n" + sales_summary + "\n\n"
        "Marketing Summary:\n" + marketing_summary
    )
    
    try:
        report_text = flan_t5_generator(report_prompt, max_length=512, min_length=150, do_sample=False, truncation=True)[0]['generated_text']
        
        # Step 2: Generate the PDF and Excel files
        # The report_text is now a coherent summary
        excel_data: List[Dict[str, Any]] = [
            {"Metric": "Total Combined Revenue", "Value": "N/A"},
            {"Metric": "Average Daily Ad Spend", "Value": "N/A"},
            {"Metric": "Average Daily Conversions", "Value": "N/A"}
        ]
        
        generate_pdf_report(report_text, filename="reports/company_report.pdf")
        generate_excel_file(excel_data, filename="reports/company_data.xlsx")
        
        return report_text
    
    except Exception as e:
        return f"Error generating final report: {e}"