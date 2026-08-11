import time

from summarizer import summarize_chunk


def benchmark_chunk(chunk):
    """
    Measure the time required to summarize one chunk.

    Parameters:
        chunk: Text chunk to summarize.

    Returns:
        A dictionary containing the generated summary and timing data.
    """

    start_time = time.perf_counter()

    summary = summarize_chunk(chunk)

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    return {
        "summary": summary,
        "time_seconds": elapsed_time
    }