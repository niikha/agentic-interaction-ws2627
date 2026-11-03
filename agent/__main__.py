import argparse

from .apicaller import call_groq_chat_completion
from .logger import Event, logger


def main() -> str:
    run_logger = logger()

    try:
        parser = argparse.ArgumentParser()

        #Get arument and log beginning of the run

        parser.add_argument("value")
        args = parser.parse_args()
        run_logger.log_event(Event.USER_TASK, args={"message": args.value})

        #call groq api with request

        completion = call_groq_chat_completion(args.value, run_logger)

        content = completion.choices[0].message.content
        run_logger.log_event(Event.FINAL, args={"message": content})
        return content
    
    except Exception as error:
        run_logger.log_event(
            Event.ERROR,
            tool="main",
            args={
                "exception_type": type(error).__name__,
                "exception": str(error),
            },
            ok=False,
        )
        raise


if __name__ == "__main__":
    print(main())
