import pymupdf


def extract_text_from_pdf(pdf_path):
    """
    Extract text from every page of a PDF.

    Parameters:
        pdf_path: Path to the PDF file.

    Returns:
        All extracted text as one string.
    """

    document = pymupdf.open(pdf_path)

    extracted_text = ""

    for page in document:
        extracted_text += page.get_text()

    document.close()

    return extracted_text