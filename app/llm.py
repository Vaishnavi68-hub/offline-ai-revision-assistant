import ollama


MODEL_NAME = "qwen2.5:3b"


def generate_response(prompt, model_name=None):
    """
    Send a prompt to the local Ollama model.

    Parameters:
        prompt: Text instruction sent to the model.
        model_name: Optional Ollama model name.

    Returns:
        Model-generated response.
    """

    if model_name is None:
        model_name = MODEL_NAME

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

    except Exception as error:

        raise RuntimeError(
            "Unable to connect to Ollama. "
            "Please make sure Ollama is running "
            f"and that the model '{model_name}' is installed."
        ) from error