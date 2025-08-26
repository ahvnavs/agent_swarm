import os # type: ignore
import requests # type: ignore
import json # type: ignore
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig # type: ignore
from typing import Any, List, Dict
import torch # type: ignore
import re # type: ignore
from .helpers import generate_pdf_report, generate_excel_file

# --- Qwen2 Model Setup ---
model_id = "Qwen/Qwen2-7B-Instruct"

# Configuration for 4-bit quantization to reduce memory usage
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

try:
    # Load Qwen2 tokenizer and model without a token
    tokenizer = AutoTokenizer.from_pretrained(model_id) # type: ignore
    model = AutoModelForCausalLM.from_pretrained( # type: ignore
        model_id,
        quantization_config=bnb_config,
        device_map="auto"
    )
except Exception as e:
    print(f"Error loading Qwen2 model: {e}")
    tokenizer = None
    model = None

def generate_final_report(sales_summary: str, marketing_summary: str) -> str:
    if tokenizer is None or model is None:
        return "Error: Qwen2 model failed to load. Cannot generate report."

    # --- Tree of Thoughts (ToT) Prompt for Qwen2 ---
    messages = [
        {"role": "system", "content": (
            "You are a professional business analyst specializing in providing detailed company performance reports. "
            "Your task is to follow the user's instructions precisely and create a comprehensive, multi-page report. "
            "Your output must be structured, factual, and actionable."
        )},
        {"role": "user", "content": (
            "TASK: Create a comprehensive company performance report. "
            "The report must contain detailed numbers, facts, and figures from the sales and marketing summaries. "
            "Include a current scenario analysis, strategic suggestions, and specific cost-cutting recommendations.\n\n"
            "--- THINKING PROCESS (Tree of Thoughts) ---\n\n"
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
            f"Here is the raw data:\n\nSales Summary:\n{sales_summary}\n\nMarketing Summary:\n{marketing_summary}"
        )}
    ]

    try:
        input_ids = tokenizer.apply_chat_template( # type: ignore
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(model.device)

        terminators = [tokenizer.eos_token_id] # type: ignore

        outputs = model.generate( # type: ignore
            input_ids, # type: ignore
            max_new_tokens=1000,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )

        report_text = tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True) # type: ignore
        
        excel_data: List[Dict[str, Any]] = [
            {"Metric": "Total Combined Revenue", "Value": "N/A"},
            {"Metric": "Average Daily Ad Spend", "Value": "N/A"},
            {"Metric": "Average Daily Conversions", "Value": "N/A"}
        ]
        
        generate_pdf_report(report_text) # type: ignore
        generate_excel_file(excel_data)
        
        return report_text # type: ignore
    
    except Exception as e:
        return f"Error generating final report: {e}"