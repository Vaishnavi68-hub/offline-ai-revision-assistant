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