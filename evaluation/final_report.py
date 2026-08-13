import csv
from collections import defaultdict


RESULTS_FILE = "results/final_benchmark_results.csv"


def main():

    with open(
        RESULTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        rows = list(
            csv.DictReader(file)
        )

    models = defaultdict(list)

    for row in rows:
        models[row["model"]].append(row)


    print("\n====================================")
    print("        FINAL BENCHMARK")
    print("====================================")


    for model, results in models.items():

        count = len(results)

        avg_time = sum(
            float(r["average_time_seconds"])
            for r in results
        ) / count

        avg_words = sum(
            float(r["average_output_words"])
            for r in results
        ) / count

        avg_speed = sum(
            float(r["words_per_second"])
            for r in results
        ) / count

        avg_coverage = sum(
            float(r["coverage_percent"])
            for r in results
        ) / count

        avg_relevance = sum(
            float(r["relevance_percent"])
            for r in results
        ) / count


        print(f"\nModel: {model}")

        print(
            f"Average inference time: "
            f"{avg_time:.2f} seconds"
        )

        print(
            f"Average output words: "
            f"{avg_words:.2f}"
        )

        print(
            f"Output speed: "
            f"{avg_speed:.2f} words/second"
        )

        print(
            f"Average coverage: "
            f"{avg_coverage:.2f}%"
        )

        print(
            f"Average relevance: "
            f"{avg_relevance:.2f}%"
        )


if __name__ == "__main__":
    main()