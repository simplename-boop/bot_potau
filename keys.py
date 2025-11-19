import os
from dotenv import load_dotenv

load_dotenv()

VK_TOKEN = os.getenv("VK_TOKEN")
PEER_ID = os.getenv("PEER_ID")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")
MY_FROM_ID = os.getenv("MI_FROM_ID")
MUR_FROM_ID = os.getenv("MUR_FROM_ID")
AND_FROM_ID = os.getenv("AND_FROM_ID")