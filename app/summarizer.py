from app.llm import generate_response


def summarize_chunk(
    text,
    model_name="qwen2.5:3b"
):
    """
    Summarize one document chunk using the
    selected local Ollama model.
    """

    prompt = f"""
You are an AI study assistant.

Summarize the following study material
for a student preparing for an exam.

Focus on:

- important concepts
- definitions
- key points
- formulas
- examples

Keep the explanation clear and concise.

Do not introduce information that is not
present in the study material.

Study material:

{text}
"""

    return generate_response(
        prompt,
        model_name
    )


def create_final_summary(
    chunk_summaries,
    model_name="qwen2.5:3b"
):
    """
    Combine individual chunk summaries into
    one final study summary.
    """

    combined_summaries = "\n\n".join(
        f"Section {i + 1}:\n{summary}"
        for i, summary in enumerate(
            chunk_summaries
        )
    )

    prompt = f"""
You are an AI revision assistant.

Create a comprehensive final study summary
from the section summaries below.

Requirements:

- Cover the most important concepts.
- Keep important definitions.
- Preserve important facts and relationships.
- Organize information using clear headings
  and bullet points.
- Remove unnecessary repetition.
- Do not introduce information that is not
  present in the provided summaries.
- Make the result useful for exam revision.

Section summaries:

{combined_summaries}
"""

    return generate_response(
        prompt,
        model_name
    )


def generate_key_points(
    chunk_summaries,
    model_name="qwen2.5:3b"
):
    """
    Generate important revision points.
    """

    combined_summaries = "\n\n".join(
        f"Section {i + 1}:\n{summary}"
        for i, summary in enumerate(
            chunk_summaries
        )
    )

    prompt = f"""
You are an AI revision assistant.

Extract the most important points from the
study material below.

Create concise exam-oriented revision notes.

Requirements:

- Focus on important concepts.
- Include important definitions.
- Include formulas or rules if present.
- Include important facts.
- Remove unnecessary explanations.
- Use bullet points.
- Do not add information that is not present
  in the material.

Study material:

{combined_summaries}
"""

    return generate_response(
        prompt,
        model_name
    )


def generate_flashcards(
    chunk_summaries,
    model_name="qwen2.5:3b"
):
    """
    Generate question-answer flashcards.
    """

    combined_summaries = "\n\n".join(
        f"Section {i + 1}:\n{summary}"
        for i, summary in enumerate(
            chunk_summaries
        )
    )

    prompt = f"""
You are an AI revision assistant.

Create useful study flashcards from the
material below.

Each flashcard must contain:

- Question
- Answer

Requirements:

- Focus on important concepts and definitions.
- Include important facts, formulas, rules,
  or relationships when present.
- Questions should test understanding
  and recall.
- Answers must be concise and accurate.
- Do not introduce information that is not
  present in the material.
- Create 10 to 15 flashcards if the material
  contains enough information.

Format the output exactly like this:

Q1: [question]
A1: [answer]

Q2: [question]
A2: [answer]

Study material:

{combined_summaries}
"""

    return generate_response(
        prompt,
        model_name
    )
