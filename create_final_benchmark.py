import csv

input_file = "results/benchmark_results.csv"
output_file = "results/final_benchmark_results.csv"

with open(input_file, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

llama_rows = [
    row for row in rows
    if row["model"] == "llama3.2:3b"
]

qwen_rows = [
    row for row in rows
    if row["model"] == "qwen2.5:3b"
]

# Keep the latest 5 Qwen results
qwen_rows = qwen_rows[-5:]

final_rows = qwen_rows + llama_rows

with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=final_rows[0].keys()
    )

    writer.writeheader()
    writer.writerows(final_rows)

print("Final benchmark rows:", len(final_rows))

for row in final_rows:
    print(
        row["model"],
        "|",
        row["topic"],
        "|",
        row["average_time_seconds"],
        "seconds"
    )
