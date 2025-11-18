import requests
from keys import DEEPSEEK_KEY


def ask_for_deepseek(prompt: str):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(url, json=data, headers=headers)
    r.raise_for_status()
    json_data = r.json()
    return json_data["choices"][0]["message"]["content"]
