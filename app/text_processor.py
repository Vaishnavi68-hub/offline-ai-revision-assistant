def create_chunks(text, chunk_size=1000, overlap=200):
    """
    Split text into overlapping word-based chunks.

    Parameters:
        text: Cleaned document text.
        chunk_size: Number of words in each chunk.
        overlap: Number of words shared between chunks.

    Returns:
        A list of text chunks.
    """

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks