import json
import os
from time import perf_counter

from dotenv import load_dotenv
from groq import Groq
from groq.types.chat import ChatCompletion

from .dataprovider import (
    CALENDAR_END_DATE,
    CALENDAR_START_DATE,
    get_calendar_entries,
)
from .logger import Event, logger

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL = os.getenv("MODEL")

MAX_TOOL_ROUNDS = 10
SYSTEM_PROMPT = (
    "Answer the user's question using calendar data. When calendar information "
    "is needed, call get_calendar_entries for the relevant date range before "
    "answering. The available calendar dates are "
    f"{CALENDAR_START_DATE.isoformat()} through {CALENDAR_END_DATE.isoformat()}. "
    "If the answer is not available in the returned data, say so."
)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_calendar_entries",
            "description": (
                "Retrieve calendar entries for an inclusive date range. "
                f"Available dates: {CALENDAR_START_DATE.isoformat()} through "
                f"{CALENDAR_END_DATE.isoformat()}."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "format": "date",
                        "description": "First calendar date, in YYYY-MM-DD format.",
                    },
                    "end_date": {
                        "type": "string",
                        "format": "date",
                        "description": "Last calendar date, in YYYY-MM-DD format.",
                    },
                },
                "required": ["start_date", "end_date"],
                "additionalProperties": False,
            },
        },
    }
]


def call_groq_chat_completion(message: str, run_logger: logger) -> ChatCompletion:
    client = Groq(api_key=API_KEY, base_url=BASE_URL)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message},
    ]

    for tool_round in range(MAX_TOOL_ROUNDS + 1):
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )
        assistant_message = completion.choices[0].message

        if not assistant_message.tool_calls:
            return completion

        if tool_round == MAX_TOOL_ROUNDS:
            raise RuntimeError(
                f"Groq exceeded the maximum of {MAX_TOOL_ROUNDS} calendar tool rounds"
            )

        messages.append(assistant_message.model_dump(mode="json", exclude_none=True))
        for tool_call in assistant_message.tool_calls:
            result = _run_calendar_tool(
                tool_call.function.name,
                tool_call.function.arguments,
                run_logger,
            )
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

    raise RuntimeError("Groq did not return a final response")


def _run_calendar_tool(name: str, arguments_json: str, run_logger: logger) -> str:
    run_logger.log_event(
        Event.TOOL_CALL,
        tool=name,
        args=arguments_json,
        model=MODEL,
    )
    started_at = perf_counter()
    result_args = None
    succeeded = False

    try:
        if name != "get_calendar_entries":
            raise ValueError(f"Unsupported Groq tool: {name}")

        arguments = json.loads(arguments_json)
        start_date = arguments["start_date"]
        end_date = arguments["end_date"]

        entries = get_calendar_entries(start_date, end_date)
        result_args = {"entries": entries}
        succeeded = True
        return json.dumps(entries)
    
    except Exception as error:
        result_args = {
            "exception_type": type(error).__name__,
            "exception": str(error),
        }
        raise

    finally:
        run_logger.log_event(
            Event.TOOL_RESULT,
            tool=name,
            args=result_args,
            ok=succeeded,
            model=MODEL,
            duration_ms=(perf_counter() - started_at) * 1000,
        )
