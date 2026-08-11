import ollama


MODEL_NAME = "qwen2.5:3b"


def generate_response(prompt):
    """
    Send a prompt to the local Ollama model.

    Parameters:
        prompt: Text instruction sent to the model.

    Returns:
        Model-generated response.
    """

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]