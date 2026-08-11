from pdf_processor import extract_text_from_pdf, clean_text


pdf_path = "data/sample_notes.pdf"

raw_text = extract_text_from_pdf(pdf_path)

cleaned_text = clean_text(raw_text)

print("===== RAW TEXT =====")
print(raw_text)

print("\n===== CLEANED TEXT =====")
print(cleaned_text)