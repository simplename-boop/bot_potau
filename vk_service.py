import requests
import time
from keys import VK_TOKEN, PEER_ID

def send_vk_msg(msg: str):
    url = "https://api.vk.com/method/messages.send"
    params = {
        "access_token": VK_TOKEN,
        "v": "5.199",
        "peer_id": PEER_ID,
        "message": msg,
        "random_id": int(time.time() * 1000),
    }
    return requests.post(url, params)

def get_histoty(count=10):
    url = "https://api.vk.com/method/messages.getHistory"
    params = {
        "access_token": VK_TOKEN,
        "v": "5.199",
        "peer_id": PEER_ID,
        "count": count,
        "rev": 0
    }

    r = requests.get(url, params=params)
    data = r.json()
    items = data["response"]["items"]
    items.reverse()

    return items
