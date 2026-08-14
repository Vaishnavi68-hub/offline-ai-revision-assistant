import time
import os
import psutil

from summarizer import summarize_chunk


def get_memory_usage_mb():
    """
    Return the current Python process memory usage in MB.
    """

    process = psutil.Process(os.getpid())

    memory_bytes = process.memory_info().rss

    memory_mb = memory_bytes / (1024 * 1024)

    return memory_mb


def benchmark_chunk(chunk):
    """
    Measure inference time, memory usage, and output size
    for one chunk.
    """

    memory_before = get_memory_usage_mb()

    start_time = time.perf_counter()

    summary = summarize_chunk(chunk)

    end_time = time.perf_counter()

    memory_after = get_memory_usage_mb()

    elapsed_time = end_time - start_time

    memory_used = memory_after - memory_before

    output_characters = len(summary)

    output_words = len(summary.split())

    return {
        "summary": summary,
        "time_seconds": elapsed_time,
        "memory_before_mb": memory_before,
        "memory_after_mb": memory_after,
        "memory_used_mb": memory_used,
        "output_characters": output_characters,
        "output_words": output_words
    }


import csv
import os


RESULTS_FILE = "results/final_benchmark_results.csv"


def load_benchmark_results():

    if not os.path.exists(RESULTS_FILE):
        return []

    results = []

    with open(
        RESULTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            results.append(row)

    return results


def calculate_model_averages(results):

    models = {}

    for result in results:

        model = result["model"]

        if model not in models:
            models[model] = []

        models[model].append(result)

    averages = {}

    for model, rows in models.items():

        count = len(rows)

        averages[model] = {
            "inference_time": sum(
                float(row["average_time_seconds"])
                for row in rows
            ) / count,

            "output_words": sum(
                float(row["average_output_words"])
                for row in rows
            ) / count,

            "speed": sum(
                float(row["words_per_second"])
                for row in rows
            ) / count,

            "coverage": sum(
                float(row["coverage_percent"])
                for row in rows
            ) / count,

            "relevance": sum(
                float(row["relevance_percent"])
                for row in rows
            ) / count
        }

    return averages