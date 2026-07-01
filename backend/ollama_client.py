import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:7b"


def ask_llm(system_prompt: str, user_prompt: str) -> str:

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

    response = requests.post(OLLAMA_URL, json=payload)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    response.raise_for_status()

    return response.json()["message"]["content"]