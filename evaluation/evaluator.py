def normalize_text(text):
    """
    Convert text into a simple normalized form.
    """

    return (
        text.lower()
        .replace(".", "")
        .replace(",", "")
        .replace(":", "")
        .replace(";", "")
    )


def calculate_coverage(summary, expected_points):
    """
    Estimate how many expected points are covered
    by the generated summary.

    Returns a percentage.
    """

    normalized_summary = normalize_text(summary)

    covered_points = 0

    for point in expected_points:

        normalized_point = normalize_text(point)

        keywords = normalized_point.split()

        important_keywords = [
            word
            for word in keywords
            if len(word) > 4
        ]

        matches = 0

        for keyword in important_keywords:

            if keyword in normalized_summary:

                matches += 1

        if important_keywords:

            match_ratio = (
                matches / len(important_keywords)
            )

            if match_ratio >= 0.5:

                covered_points += 1

    coverage = (
        covered_points / len(expected_points)
    ) * 100

    return coverage