import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion

from .logger import logger
from .tools.toolprovider import toolprovider

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL = os.getenv("MODEL")

MAX_TOOL_ROUNDS = 10
SYSTEM_PROMPT = (
    "Answer the user's question using calendar data. When calendar information "
    "is needed, call get_calendar_entries for the relevant date before "
    "answering. "
    "If the answer is not available in the returned data, say so."
)


def call_openai_chat_completion(message: str, run_logger: logger) -> ChatCompletion:
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    tool_provider = toolprovider(run_logger, MODEL)
    tool_definitions = tool_provider.get_tool_definitions()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message},
    ]

    for tool_round in range(MAX_TOOL_ROUNDS + 1):
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tool_definitions,
            tool_choice="auto",
        )
        assistant_message = completion.choices[0].message

        if not assistant_message.tool_calls:
            return completion

        if tool_round == MAX_TOOL_ROUNDS:
            raise RuntimeError(
                f"OpenAI exceeded the maximum of {MAX_TOOL_ROUNDS} calendar tool rounds"
            )

        messages.append(assistant_message.model_dump(mode="json", exclude_none=True))
        for tool_call in assistant_message.tool_calls:
            result = tool_provider.run_tool(
                tool_call.function.name,
                tool_call.function.arguments,
            )
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

    raise RuntimeError("OpenAI did not return a final response")
