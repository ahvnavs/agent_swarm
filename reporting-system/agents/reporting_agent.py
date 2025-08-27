import os
import requests
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import openpyxl
import pandas as pd
from groq import Groq
import httpx
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText  
from email import encoders

class ReportingAgent:
    """
    An agent to synthesize summaries and generate final reports.
    """
    def __init__(self):
        self.report_dir = "reports"
        self.today_date = date.today().strftime("%Y-%m-%d")

        self.api_key = os.environ.get("LLM_API_KEY")

        if "http_proxy" in os.environ:
            del os.environ["http_proxy"]
        if "https_proxy" in os.environ:
            del os.environ["https_proxy"]

        http_client = httpx.Client(proxies={})
        self.client = Groq(api_key=self.api_key, http_client=http_client)
        self.model_name = "llama3-8b-8192"
        
    def create_combined_summary(self, sales_summary, marketing_summary):
        """
        Combines summaries from other agents into a detailed, single paragraph.
        """
        if "Error:" in sales_summary or "Error:" in marketing_summary:
            return "Note: A detailed report could not be generated due to missing information from one or more agents."

        try:
            prompt = (
                f"You are a senior business analyst compiling a daily company performance report. "
                f"Take the following two summaries and synthesize them into a single, detailed, "
                f"multi-paragraph executive summary. The tone should be professional and highlight "
                f"key achievements and areas for improvement. Do not use bullet points.\n\n"
                f"Sales Summary: {sales_summary}\n\n"
                f"Marketing Summary: {marketing_summary}"
            )
            
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                temperature=0.7,
                max_tokens=512
            )
            
            combined_summary = chat_completion.choices[0].message.content.strip()
            return combined_summary

        except Exception as e:
            return f"Error: An error occurred while generating the combined summary. Details: {e}"

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
        return filename

    def create_pdf_report(self, sales_summary, marketing_summary, combined_summary):
        """Creates a professional, multi-page PDF report with a combined summary."""
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

        story.append(Paragraph("<b>Executive Summary</b>", styles['Normal']))
        story.append(Spacer(1, 6))
        story.append(Paragraph(combined_summary, styles['Normal']))
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
        return filename

    def create_excel_report(self, sales_data, marketing_data):
        """Creates an Excel file with actual metrics."""
        filename = os.path.join(self.report_dir, "company_data.xlsx")
        
        sales_revenue = sales_data.get('total_revenue') if isinstance(sales_data, dict) else 0
        sales_customers = sales_data.get('new_customers') if isinstance(sales_data, dict) else 0
        marketing_spend = marketing_data.get('ad_spend') if isinstance(marketing_data, dict) else 0
        marketing_impressions = marketing_data.get('impressions') if isinstance(marketing_data, dict) else 0

        data = {
            'Metric': ['Revenue', 'New Customers', 'Ad Spend', 'Impressions'],
            'Value': [sales_revenue, sales_customers, marketing_spend, marketing_impressions],
            'Date': [self.today_date, self.today_date, self.today_date, self.today_date]
        }
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Generated Excel report: {filename}")
        return filename

    def send_email_with_reports(self, pdf_file, excel_file):
        """Sends an email with the PDF and Excel reports attached."""
        sender_email = os.environ.get("EMAIL_SENDER")
        sender_password = os.environ.get("EMAIL_PASSWORD")
        recipient_email = os.environ.get("EMAIL_RECIPIENT")
        smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.environ.get("SMTP_PORT", 587))

        if not all([sender_email, sender_password, recipient_email]):
            print("Error: Email credentials or recipient not set in environment variables. Skipping email.")
            return

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = f"Daily Company Performance Report - {self.today_date}"

        body = (
            "Dear team,\n\n"
            "Please find attached the daily company performance report for today, "
            f"{self.today_date}. The report includes a detailed executive summary, "
            "as well as the raw data in an Excel format.\n\n"
            "Best regards,\n"
            "The Reporting Agent"
        )
        message.attach(MIMEText(body, "plain"))

        for file_path in [pdf_file, excel_file]:
            if os.path.exists(file_path):
                with open(file_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {os.path.basename(file_path)}",
                )
                message.attach(part)

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")