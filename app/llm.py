import os
import ollama

from cloud_llm import generate_cloud_response

MODEL_NAME = "qwen2.5:3b"


def get_ai_backend():
    """
    Determine which AI backend to use.

    AI_BACKEND=cloud
        Hugging Face cloud inference.

    AI_BACKEND=local
        Local Ollama inference.

    Defaults to local for development.
    """

    return os.getenv(
        "AI_BACKEND",
        "local"
    ).lower().strip()


def generate_response(
    prompt,
    model_name=None
):
    """
    Generate an AI response using either
    Hugging Face Cloud or local Ollama.
    """

    backend = get_ai_backend()

    # ==============================================
    # HUGGING FACE CLOUD
    # ==============================================

    if backend == "cloud":

        try:

            return generate_cloud_response(prompt)

        except Exception as error:

            raise RuntimeError(
                f"Cloud AI generation failed: {error}"
            ) from error

    # ==============================================
    # LOCAL OLLAMA
    # ==============================================

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
