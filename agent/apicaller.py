import os

from dotenv import load_dotenv
from groq import Groq
from groq.types.chat import ChatCompletion

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL = os.getenv("MODEL")


def call_groq_chat_completion(message: str) -> ChatCompletion:
    client = Groq(api_key=API_KEY, base_url=BASE_URL)
    return client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": message}],
    )
