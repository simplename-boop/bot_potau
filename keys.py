import os
from dotenv import load_dotenv

load_dotenv()

VK_TOKEN = os.getenv("VK_TOKEN")
PEER_ID = os.getenv("PEER_ID")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")