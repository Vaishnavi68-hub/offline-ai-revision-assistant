import csv
import os


RESULTS_FILE = "results/benchmark_results.csv"


def load_results():

    if not os.path.exists(RESULTS_FILE):

        print(
            "Benchmark results file not found."
        )

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


def generate_report(results):

    if not results:

        print("No benchmark results available.")

        return

    models = {}

    for result in results:

        model = result["model"]

        if model not in models:

            models[model] = []

        models[model].append(result)


    print("\n====================================")
    print("       BENCHMARK REPORT")
    print("====================================")


    for model, model_results in models.items():

        total_time = 0
        total_coverage = 0
        total_relevance = 0

        for result in model_results:

            total_time += float(
                result["average_time_seconds"]
            )

            total_coverage += float(
                result["coverage_percent"]
            )

            total_relevance += float(
                result["relevance_percent"]
            )


        count = len(model_results)

        average_time = (
            total_time / count
        )

        average_coverage = (
            total_coverage / count
        )

        average_relevance = (
            total_relevance / count
        )


        print("\nModel:", model)

        print(
            f"Average inference time: "
            f"{average_time:.2f} seconds"
        )

        print(
            f"Average coverage: "
            f"{average_coverage:.2f}%"
        )

        print(
            f"Average relevance: "
            f"{average_relevance:.2f}%"
        )


if __name__ == "__main__":

    results = load_results()

    generate_report(results)