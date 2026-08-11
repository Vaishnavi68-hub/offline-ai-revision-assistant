from pdf_processor import extract_text_from_pdf, clean_text
from text_processor import create_chunks
from summarizer import summarize_chunk, generate_key_points


pdf_path = "data/sample_notes.pdf"

raw_text = extract_text_from_pdf(pdf_path)

cleaned_text = clean_text(raw_text)

chunks = create_chunks(
    cleaned_text,
    chunk_size=100,
    overlap=20
)

print("Number of chunks:", len(chunks))

if not chunks:
    print("No chunks were created.")
    exit()


chunk_summaries = []

for i, chunk in enumerate(chunks):

    print(f"Summarizing chunk {i + 1}/{len(chunks)}...")

    summary = summarize_chunk(chunk)

    chunk_summaries.append(summary)


print("\nGenerating key points...")

key_points = generate_key_points(chunk_summaries)

print("\n==============================")
print("KEY REVISION POINTS")
print("==============================\n")

print(key_points)