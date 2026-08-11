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


from evaluation_dataset import EVALUATION_DATASET
from summarizer import summarize_chunk


def run_evaluation():

    results = []

    for item in EVALUATION_DATASET:

        print("\n==============================")
        print(f"Topic: {item['topic']}")
        print("==============================")

        print("\nGenerating summary...")

        summary = summarize_chunk(item["text"])

        print("\nGenerated Summary:")
        print(summary)

        results.append(
            {
                "topic": item["topic"],
                "text": item["text"],
                "expected_points": item["expected_points"],
                "generated_summary": summary
            }
        )

    return results


if __name__ == "__main__":

    run_evaluation()