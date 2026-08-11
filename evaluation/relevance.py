def calculate_relevance(summary, keywords):
    """
    Calculate how many topic-specific keywords
    appear in the generated summary.

    Returns:
        Relevance score as a percentage.
    """

    normalized_summary = summary.lower()

    matched_keywords = 0

    for keyword in keywords:

        if keyword.lower() in normalized_summary:
            matched_keywords += 1

    relevance = (
        matched_keywords / len(keywords)
    ) * 100

    return relevance