from pdf_processor import extract_text_from_pdf, clean_text
from text_processor import create_chunks
from benchmark import benchmark_chunk


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


times = []
memory_usage = []


for i, chunk in enumerate(chunks):

    print(
        f"\nBenchmarking chunk {i + 1}/{len(chunks)}..."
    )

    result = benchmark_chunk(chunk)

    times.append(result["time_seconds"])

    memory_usage.append(
        result["memory_used_mb"]
    )

    print(
        f"Time: {result['time_seconds']:.2f} seconds"
    )

    print(
        f"Memory change: "
        f"{result['memory_used_mb']:.2f} MB"
    )


total_time = sum(times)

average_time = total_time / len(times)

average_memory = sum(memory_usage) / len(memory_usage)


print("\n==============================")
print("BENCHMARK RESULTS")
print("==============================")

print(
    f"Total inference time: "
    f"{total_time:.2f} seconds"
)

print(
    f"Average time per chunk: "
    f"{average_time:.2f} seconds"
)

print(
    f"Average Python process memory change: "
    f"{average_memory:.2f} MB"
)