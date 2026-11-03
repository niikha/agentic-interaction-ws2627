import os
from time import perf_counter

from dotenv import load_dotenv
from groq import Groq
from groq.types.chat import ChatCompletion

from .dataprovider import get_calendar_entries
from .logger import Event, logger

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL = os.getenv("MODEL")


def call_groq_chat_completion(message: str, run_logger: logger) -> ChatCompletion:

    #Get calendar entries (initial plan was to add calendar entries as 
    #documents parameter, but some models on groq don't support this)

    message_with_calendar = "\n\n".join([*get_calendar_entries(), message])

    #create request and log it

    client = Groq(api_key=API_KEY, base_url=BASE_URL)
    arguments = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Answer using only the provided documents. If the answer isn't in them, say so."},
            {"role": "user", "content": message_with_calendar},
        ],
    }
    tool = "groq.chat.completions.create"
    run_logger.log_event(Event.TOOL_CALL, tool=tool, args=arguments, model=MODEL)

    #get response and log it
    
    api_call_started_at = perf_counter()
    result_args = None
    succeeded = False

    try:
        completion = client.chat.completions.create(**arguments)
        result_args = completion.model_dump(mode="json")
        succeeded = True
        return completion
    
    except Exception as error:
        result_args = {
            "exception_type": type(error).__name__,
            "exception": str(error),
        }
        raise

    finally:
        run_logger.log_event(
            Event.TOOL_RESULT,
            tool=tool,
            args=result_args,
            ok=succeeded,
            model=MODEL,
            duration_ms=(perf_counter() - api_call_started_at) * 1000,
        )
