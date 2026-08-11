from pdf_processor import extract_text_from_pdf, clean_text
from text_processor import create_chunks
from summarizer import summarize_chunk


pdf_path = "data/sample_notes.pdf"

raw_text = extract_text_from_pdf(pdf_path)

cleaned_text = clean_text(raw_text)

chunks = create_chunks(
    cleaned_text,
    chunk_size=100,
    overlap=20
)

print("Number of chunks:", len(chunks))

if chunks:
    print("\n===== ORIGINAL CHUNK =====")
    print(chunks[0])

    print("\n===== AI SUMMARY =====")

    summary = summarize_chunk(chunks[0])

    print(summary)
else:
    print("No chunks were created.")