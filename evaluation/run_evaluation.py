import sys
import os
import time

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "app"
        )
    )
)

sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__)
    )
)

from evaluation_dataset import EVALUATION_DATASET
from summarizer import summarize_chunk
from evaluator import calculate_coverage
from relevance import calculate_relevance


def run_evaluation():

    results = []

    number_of_runs = 3

    for item in EVALUATION_DATASET:

        print("\n==============================")
        print(f"Topic: {item['topic']}")
        print("==============================")

        run_times = []

        final_summary = ""

        for run_number in range(1, number_of_runs + 1):

            print(
                f"\nRun {run_number}/{number_of_runs}"
            )

            start_time = time.perf_counter()

            summary = summarize_chunk(
                item["text"]
            )

            end_time = time.perf_counter()

            elapsed_time = (
                end_time - start_time
            )

            run_times.append(
                elapsed_time
            )

            final_summary = summary

            print(
                f"Inference time: "
                f"{elapsed_time:.2f} seconds"
            )

        average_time = (
            sum(run_times) / len(run_times)
        )

        coverage_score = calculate_coverage(
            final_summary,
            item["expected_points"]
        )

        relevance_score = calculate_relevance(
            final_summary,
            item["keywords"]
        )

        print("\nFinal Generated Summary:")
        print(final_summary)

        print(
            f"\nAverage Inference Time: "
            f"{average_time:.2f} seconds"
        )

        print(
            f"Coverage Score: "
            f"{coverage_score:.2f}%"
        )

        print(
            f"Relevance Score: "
            f"{relevance_score:.2f}%"
        )

        results.append(
            {
                "topic": item["topic"],
                "average_time": average_time,
                "coverage": coverage_score,
                "relevance": relevance_score
            }
        )

    return results


if __name__ == "__main__":

    print("Starting evaluation...")

    run_evaluation()

    print("\nEvaluation complete.")