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


def get_recommended_model(averages):

    if not averages:
        return None

    return min(
        averages.keys(),
        key=lambda model: (
            -averages[model]["relevance"],
            -averages[model]["coverage"],
            averages[model]["inference_time"]
        )
    )