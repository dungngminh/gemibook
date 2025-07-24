from pdfminer.high_level import extract_text

def get_pdf_text(pdf_path):
    """
    Extracts text from a PDF file.
    """
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None
