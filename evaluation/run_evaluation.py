import sys
import os

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

    for item in EVALUATION_DATASET:

        print("\n==============================")
        print(f"Topic: {item['topic']}")
        print("==============================")

        print("\nGenerating summary...")

        summary = summarize_chunk(
            item["text"]
        )

        coverage_score = calculate_coverage(
            summary,
            item["expected_points"]
        )

        relevance_score = calculate_relevance(
            summary,
            item["keywords"]
        )

        print("\nGenerated Summary:")
        print(summary)

        print(
            f"\nCoverage Score: "
            f"{coverage_score:.2f}%"
        )

        print(
            f"Relevance Score: "
            f"{relevance_score:.2f}%"
        )

        results.append(
            {
                "topic": item["topic"],
                "coverage": coverage_score,
                "relevance": relevance_score
            }
        )

    return results


if __name__ == "__main__":

    run_evaluation()