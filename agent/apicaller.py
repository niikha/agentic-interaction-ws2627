from groq import Groq
from groq.types.chat import ChatCompletion

GROQ_API_KEY = "YOUR_GROQ_API_KEY"
GROQ_MODEL = "YOUR_GROQ_MODEL"


def call_groq_chat_completion(message: str) -> ChatCompletion:
    client = Groq(api_key=GROQ_API_KEY)
    return client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": message}],
    )
