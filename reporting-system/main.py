import sys
import os
from datetime import datetime
from agents.sales_agent import SalesAgent
from agents.marketing_agent import MarketingAgent
from agents.reporting_agent import ReportingAgent

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_report_generation():
    """
    Main function to orchestrate the report generation process.
    """
    print(f"[{datetime.now()}] Starting daily report generation...")
    
    sales_agent = SalesAgent()
    marketing_agent = MarketingAgent()
    reporting_agent = ReportingAgent()
    
    sales_data = sales_agent.get_data()
    marketing_data = marketing_agent.get_data()
    
    sales_summary = sales_agent.get_summary(sales_data)
    marketing_summary = marketing_agent.get_summary(marketing_data)
    
    final_sales_summary = sales_summary
    final_marketing_summary = marketing_summary
    
    if isinstance(sales_summary, str) and sales_summary.startswith("Error:"):
        print(f"Warning: Sales agent failed. {sales_summary}")
        final_sales_summary = f"Error fetching sales data. Reason: {sales_summary.split(':', 1)[1].strip()}"
    
    if isinstance(marketing_summary, str) and marketing_summary.startswith("Error:"):
        print(f"Warning: Marketing agent failed. {marketing_summary}")
        final_marketing_summary = f"Error fetching marketing data. Reason: {marketing_summary.split(':', 1)[1].strip()}"
    
    combined_summary = reporting_agent.create_combined_summary(final_sales_summary, final_marketing_summary)
    
    text_file = reporting_agent.create_text_report(final_sales_summary, final_marketing_summary)
    pdf_file = reporting_agent.create_pdf_report(final_sales_summary, final_marketing_summary, combined_summary)
    excel_file = reporting_agent.create_excel_report(sales_data, marketing_data)
    
    reporting_agent.send_email_with_reports(pdf_file, excel_file)
    
    print(f"[{datetime.now()}] Daily report generation complete.")

if __name__ == "__main__":
    run_report_generation()
