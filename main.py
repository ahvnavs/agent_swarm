import os
import smtplib
from email.message import EmailMessage
import time
from dotenv import load_dotenv

from agents.sales_agent import get_sales_data_and_summary
from agents.marketing_agent import get_marketing_data_and_summary
from agents.reporting_agent import generate_final_report

load_dotenv()

def run_report_generation():
    print("--- Running daily report generation ---")

    sales_summary = get_sales_data_and_summary()
    marketing_summary = get_marketing_data_and_summary()

    if "Error:" in sales_summary:
        print("Sales agent failed, providing a fallback message.")
        sales_summary = "Sales data could not be retrieved. The Sales API may be down."
    
    if "Error:" in marketing_summary:
        print("Marketing agent failed, providing a fallback message.")
        marketing_summary = "Marketing data could not be retrieved. The Marketing API may be down."

    final_report = generate_final_report(sales_summary, marketing_summary)

    report_path = f"daily_report_{time.strftime('%Y-%m-%d')}.txt"
    if final_report:
        with open(report_path, "w") as f:
            f.write(final_report)
        print(f"\nReport saved to {report_path}")

    try:
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        receiver_email = os.getenv("RECEIVER_EMAIL")

        if not sender_email or not sender_password or not receiver_email:
            raise ValueError("Email environment variables are not set. Cannot send email.")

        msg = EmailMessage()
        msg['Subject'] = "Daily Company Performance Report"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        email_content = final_report if final_report else "Report could not be generated."
        msg.set_content(email_content)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("Report email sent successfully!")

    except ValueError as e:
        print(f"Failed to send email: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during report generation: {e}")

if __name__ == "__main__":
    run_report_generation()