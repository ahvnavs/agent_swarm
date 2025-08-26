from fpdf import FPDF
from openpyxl import Workbook
import re
from typing import List, Dict, Any

def generate_pdf_report(report_text: str, filename: str = "company_report.pdf"):
    """Generates a multi-page PDF report from a string."""
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pages = re.split(r'\n\s*PAGE\s*\d+\s*', report_text, flags=re.IGNORECASE)

        for i, page_content in enumerate(pages):
            if i > 0:
                pdf.add_page()
            pdf.multi_cell(0, 10, page_content.strip())  # type: ignore

        pdf.output(filename)
        return True
    except Exception as e:
        print(f"Error generating PDF report: {e}")
        return False

def generate_excel_file(report_details: List[Dict[str, Any]], filename: str = "company_data.xlsx"):
    """Generates an Excel file from structured data."""
    try:
        if not report_details:
            print("No data provided for Excel file. Skipping Excel generation.")
            return False

        wb = Workbook()
        ws = wb.active
        ws.title = "Report Metrics" # type: ignore

        headers = list(report_details[0].keys())
        ws.append(headers) # type: ignore

        for row in report_details:
            ws.append(list(row.values())) # type: ignore

        wb.save(filename)
        return True
    except Exception as e:
        print(f"Error generating Excel file: {e}")
        return False