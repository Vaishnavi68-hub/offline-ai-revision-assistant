import ollama


DEFAULT_MODEL = "llama3.2:3b"


def generate_response(
    prompt,
    model_name=DEFAULT_MODEL
):
    """
    Send a prompt to the selected local Ollama model.

    Parameters:
        prompt: Text instruction sent to the model.
        model_name: Ollama model to use.

    Returns:
        Model-generated response.
    """

    try:

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

    except Exception as e:

        raise RuntimeError(
            f"Unable to connect to Ollama or use model "
            f"'{model_name}'. "
            "Please make sure Ollama is running "
            "and the selected model is installed."
        ) from e