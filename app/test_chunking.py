from pdf_processor import extract_text_from_pdf, clean_text
from text_processor import create_chunks


pdf_path = "data/sample_notes.pdf"

raw_text = extract_text_from_pdf(pdf_path)

print("Raw text length:", len(raw_text))

cleaned_text = clean_text(raw_text)

print("Cleaned text length:", len(cleaned_text))

print("\nFirst 500 characters:")
print(cleaned_text[:500])

chunks = create_chunks(
    cleaned_text,
    chunk_size=100,
    overlap=20
)

print("\nNumber of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\n===== CHUNK {i + 1} =====")
    print(chunk)