import os

from dotenv import load_dotenv
from groq import Groq
from groq.types.chat import ChatCompletion

from .dataprovider import dataprovider

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL = os.getenv("MODEL")


def call_groq_chat_completion(message: str) -> ChatCompletion:
    #get calendar data for context
    documents = [
        {"source": {"type": "text", "text": entry}}
        for entry in dataprovider().get_calendar_entries()
    ]
    client = Groq(api_key=API_KEY, base_url=BASE_URL)
    return client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": message}],
        documents=documents,
    )
