from pdf_processor import extract_text_from_pdf, clean_text
from text_processor import create_chunks
from summarizer import summarize_chunk, create_final_summary


pdf_path = "data/sample_notes.pdf"

print("Reading PDF...")

raw_text = extract_text_from_pdf(pdf_path)

cleaned_text = clean_text(raw_text)

print("Creating chunks...")

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

    print(f"\nSummarizing chunk {i + 1}/{len(chunks)}...")

    summary = summarize_chunk(chunk)

    chunk_summaries.append(summary)

print("\nAll chunks summarized.")

print("\nCreating final summary...")

final_summary = create_final_summary(chunk_summaries)

print("\n==============================")
print("FINAL STUDY SUMMARY")
print("==============================\n")

print(final_summary)