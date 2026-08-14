import os

from huggingface_hub import InferenceClient


def generate_cloud_response(
    prompt,
    model="Qwen/Qwen2.5-3B-Instruct"
):
    """
    Generate a response using a Hugging Face hosted model.
    """

    token = os.getenv("HF_TOKEN")

    if not token:
        raise RuntimeError(
            "HF_TOKEN is not configured."
        )

    client = InferenceClient(
        provider="auto",
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