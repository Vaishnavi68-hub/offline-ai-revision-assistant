import ollama


MODEL_NAME = "llama3.2:3b"


def generate_response(
    prompt,
    model_name=MODEL_NAME
):
    """
    Send a prompt to a local Ollama model.

    Parameters:
        prompt: Text instruction sent to the model.
        model_name: Name of the Ollama model to use.

    Returns:
        Model-generated response.
    """

    response = ollama.chat(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]