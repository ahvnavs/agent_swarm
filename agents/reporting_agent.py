import os
import requests # type: ignore
import json # type: ignore
from transformers import AutoTokenizer, AutoModelForCausalLM # type: ignore
from typing import Any, List, Dict # type: ignore
import torch # type: ignore
import re # type: ignore
from .helpers import generate_pdf_report, generate_excel_file
from pydantic import BaseModel, Field # type: ignore

# 1. Model loading is moved outside the function to load only once
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

# Check for a Hugging Face token in the environment
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError("Hugging Face token not found. Please set the HF_TOKEN environment variable.")

try:
    # Load Llama 3 tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_token) # type: ignore
    model = AutoModelForCausalLM.from_pretrained( # type: ignore
        model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        token=hf_token
    )
except Exception as e:
    print(f"Error loading Llama 3 model: {e}")
    tokenizer = None
    model = None

# Define a Pydantic model for the excel data to ensure type safety
class ReportMetric(BaseModel):
    Metric: str
    Value: Any

def generate_final_report(sales_summary: str, marketing_summary: str) -> str:
    if tokenizer is None or model is None:
        return "Error: Llama 3 model failed to load. Cannot generate report."

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
    
    messages = [
        {"role": "system", "content": "You are a professional business analyst."},
        {"role": "user", "content": tot_prompt},
    ]

    try:
        inputs = tokenizer.apply_chat_template( # type: ignore
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(model.device)

        terminators = [ # type: ignore
            tokenizer.eos_token_id, # type: ignore
            tokenizer.convert_tokens_to_ids("<|eot_id|>") # type: ignore
        ]

        outputs = model.generate( # type: ignore
            inputs, # type: ignore
            max_new_tokens=1000,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        report_text = tokenizer.decode(outputs[0][inputs.shape[-1]:], skip_special_tokens=True) # type: ignore
        
        # Extract a simplified placeholder for the Excel file
        excel_data = [
            {"Metric": "Total Combined Revenue", "Value": "N/A"},
            {"Metric": "Average Daily Ad Spend", "Value": "N/A"},
            {"Metric": "Average Daily Conversions", "Value": "N/A"}
        ]
        
        generate_pdf_report(report_text) # type: ignore
        generate_excel_file(excel_data)
        
        return report_text # type: ignore
    
    except Exception as e:
        return f"Error generating final report: {e}"