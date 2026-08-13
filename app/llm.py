import ollama


MODEL_NAME = "llama3.2:3b"


def generate_response(prompt):
    """
    Send a prompt to the local Ollama model.
    """

    try:

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

    except Exception as e:

        raise RuntimeError(
            "Unable to connect to Ollama. "
            "Please make sure Ollama is running "
            "and the model 'llama3.2:3b' is available."
        ) from e