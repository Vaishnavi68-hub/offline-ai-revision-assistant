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


def calculate_coverage(
    summary,
    expected_points
):
    """
    Estimate how many expected points are covered
    by the generated summary.

    Returns:
        Coverage percentage between 0 and 100.
    """

    if not expected_points:
        return 0.0

    normalized_summary = normalize_text(
        summary
    )

    covered_points = 0

    total_points = len(
        expected_points
    )

    for point in expected_points:

        normalized_point = normalize_text(
            point
        )

        keywords = normalized_point.split()

        important_keywords = [
            word
            for word in keywords
            if len(word) > 4
        ]

        if not important_keywords:
            continue

        matches = 0

        for keyword in important_keywords:

            if keyword in normalized_summary:

                matches += 1

        match_ratio = (
            matches / len(important_keywords)
        )

        if match_ratio >= 0.5:

            covered_points += 1

    coverage = (
        covered_points / total_points
    ) * 100

    # Coverage must always be between 0 and 100.
    coverage = max(
        0.0,
        min(
            100.0,
            coverage
        )
    )

    return coverage