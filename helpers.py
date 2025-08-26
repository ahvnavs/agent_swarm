# helpers.py
from fpdf import FPDF
from openpyxl import Workbook
import re

def generate_pdf_report(report_text, filename="company_report.pdf"):
    """Generates a multi-page PDF report from a string."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto_page_break=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Use a regex to split the report into "pages" for simplicity
    pages = re.split(r'\n\s*PAGE\s*\d+\s*', report_text, flags=re.IGNORECASE)

    for i, page_content in enumerate(pages):
        if i > 0:
            pdf.add_page()
        pdf.multi_cell(0, 10, page_content.strip())

    pdf.output(filename)

def generate_excel_file(report_details, filename="company_data.xlsx"):
    """Generates an Excel file from structured data."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Report Metrics"

    # Write headers
    headers = list(report_details[0].keys())
    ws.append(headers)

    # Write data
    for row in report_details:
        ws.append(list(row.values()))

    wb.save(filename)