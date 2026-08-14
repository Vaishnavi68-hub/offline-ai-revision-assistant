import os

from huggingface_hub import InferenceClient


MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"


def generate_cloud_response(
    prompt,
    model=MODEL_NAME
):
    """
    Generate a response using a Hugging Face
    Inference Provider.
    """

    token = os.getenv("HF_TOKEN")

    if not token:
        raise RuntimeError(
            "HF_TOKEN is not configured."
        )

    client = InferenceClient(
        provider="featherless-ai",
        api_key=token
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1000,
        temperature=0.3
    )

    return response.choices[0].message.content