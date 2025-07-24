import pytest
from bookbot.pdf_parser import get_pdf_text
from PyPDF2 import PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

@pytest.fixture(scope="module")
def create_test_pdf(tmp_path_factory):
    pdf_path = tmp_path_factory.mktemp("data") / "test_document.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 750, "Hello, this is a test PDF.")
    c.drawString(100, 730, "It has multiple lines of text.")
    c.save()
    return str(pdf_path)

def test_get_pdf_text(create_test_pdf):
    pdf_path = create_test_pdf
    extracted_text = get_pdf_text(pdf_path)
    assert "Hello, this is a test PDF." in extracted_text
    assert "It has multiple lines of text." in extracted_text

def test_get_pdf_text_non_existent_file():
    extracted_text = get_pdf_text("non_existent.pdf")
    assert extracted_text is None

def test_get_pdf_text_empty_file(tmp_path_factory):
    pdf_path = tmp_path_factory.mktemp("data") / "empty.pdf"
    PdfWriter().write(open(pdf_path, "wb"))
    extracted_text = get_pdf_text(str(pdf_path))
    assert extracted_text == ""
