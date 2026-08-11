import sys
import os
import time
import csv
from datetime import datetime


MODEL_NAME = "qwen2.5:3b"


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


def save_results(results):

    os.makedirs(
        "results",
        exist_ok=True
    )

    file_path = (
        "results/benchmark_results.csv"
    )

    file_exists = os.path.exists(
        file_path
    )

    with open(
        file_path,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow(
                [
                    "timestamp",
                    "model",
                    "topic",
                    "average_time_seconds",
                    "coverage_percent",
                    "relevance_percent"
                ]
            )

        timestamp = datetime.now().isoformat()

        for result in results:

            writer.writerow(
                [
                    timestamp,
                    MODEL_NAME,
                    result["topic"],
                    round(
                        result["average_time"],
                        2
                    ),
                    round(
                        result["coverage"],
                        2
                    ),
                    round(
                        result["relevance"],
                        2
                    )
                ]
            )


if __name__ == "__main__":

    print("Starting evaluation...")

    results = run_evaluation()

    save_results(results)

    print("\nResults saved to:")
    print(
        "results/benchmark_results.csv"
    )

    print("\nEvaluation complete.")