import os
from datetime import datetime
from agents.sales_agent import SalesAgent
from agents.marketing_agent import MarketingAgent
from agents.reporting_agent import ReportingAgent

def run_report_generation():
    """
    Main function to orchestrate the report generation process.
    """
    print(f"[{datetime.now()}] Starting daily report generation...")
    
    # Initialize agents
    sales_agent = SalesAgent()
    marketing_agent = MarketingAgent()
    reporting_agent = ReportingAgent()
    
    # Execute agents and get summaries
    sales_summary = sales_agent.get_summary()
    marketing_summary = marketing_agent.get_summary()
    
    final_sales_summary = sales_summary
    final_marketing_summary = marketing_summary
    
    # Error Handling & Fallback
    if sales_summary.startswith("Error:"):
        print(f"Warning: Sales agent failed. {sales_summary}")
        final_sales_summary = f"Error fetching sales data. Reason: {sales_summary.split(':', 1)[1].strip()}"
    
    if marketing_summary.startswith("Error:"):
        print(f"Warning: Marketing agent failed. {marketing_summary}")
        final_marketing_summary = f"Error fetching marketing data. Reason: {marketing_summary.split(':', 1)[1].strip()}"
        
    # Generate final reports
    reporting_agent.create_text_report(final_sales_summary, final_marketing_summary)
    reporting_agent.create_pdf_report(final_sales_summary, final_marketing_summary)
    reporting_agent.create_excel_report()
    
    print(f"[{datetime.now()}] Daily report generation complete.")

if __name__ == "__main__":
    run_report_generation()