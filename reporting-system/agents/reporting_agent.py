from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import openpyxl
import pandas as pd
import os

class ReportingAgent:
    """
    An agent to synthesize summaries and generate final reports.
    """
    def __init__(self):
        self.report_dir = "reports"
        self.today_date = date.today().strftime("%Y-%m-%d")
        
    def create_text_report(self, sales_summary, marketing_summary):
        """Creates a clean text report."""
        filename = os.path.join(self.report_dir, f"daily_report_{self.today_date}.txt")
        with open(filename, "w") as f:
            f.write(f"Daily Company Performance Report - {self.today_date}\n")
            f.write("-" * 50 + "\n\n")
            f.write("1. Sales Performance Summary\n")
            f.write("----------------------------\n")
            f.write(sales_summary + "\n\n")
            f.write("2. Marketing Campaign Summary\n")
            f.write("-----------------------------\n")
            f.write(marketing_summary + "\n\n")
        print(f"Generated text report: {filename}")

    def create_pdf_report(self, sales_summary, marketing_summary):
        """Creates a professional, multi-page PDF report."""
        filename = os.path.join(self.report_dir, "company_report.pdf")
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        title = Paragraph(f"Daily Company Performance Report", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        subtitle = Paragraph(f"Report Date: {self.today_date}", styles['Normal'])
        story.append(subtitle)
        story.append(Spacer(1, 24))

        story.append(Paragraph("<b>1. Sales Performance Summary</b>", styles['Normal']))
        story.append(Spacer(1, 6))
        story.append(Paragraph(sales_summary, styles['Normal']))
        story.append(Spacer(1, 24))

        story.append(Paragraph("<b>2. Marketing Campaign Summary</b>", styles['Normal']))
        story.append(Spacer(1, 6))
        story.append(Paragraph(marketing_summary, styles['Normal']))
        story.append(Spacer(1, 24))

        doc.build(story)
        print(f"Generated PDF report: {filename}")

    def create_excel_report(self, sales_data=None, marketing_data=None):
        """Creates an Excel file with placeholder metrics."""
        filename = os.path.join(self.report_dir, "company_data.xlsx")
        data = {
            'Metric': ['Revenue', 'New Customers', 'Ad Spend', 'Impressions'],
            'Value': [0, 0, 0, 0],  # Placeholder values
            'Date': [self.today_date, self.today_date, self.today_date, self.today_date]
        }
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Generated Excel report: {filename}")