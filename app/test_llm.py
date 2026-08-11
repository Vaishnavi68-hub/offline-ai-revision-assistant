from llm import generate_response


prompt = """
Explain what a process is in operating systems.
Give the answer in 3 simple sentences.
"""

response = generate_response(prompt)

print("===== MODEL RESPONSE =====")
print(response)