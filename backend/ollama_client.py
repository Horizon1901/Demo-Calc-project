import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:7b"


def ask_llm(system_prompt: str, user_prompt: str) -> str:
    # This prepares the main payload or the envelope that will be sent to the LLM API. It contains the model name, the system prompt, and the user prompt.
    payload = {
        "model": MODEL,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    }
    # Sends the request 
    response = requests.post(OLLAMA_URL, json=payload)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    response.raise_for_status()

    return response.json()["message"]["content"]