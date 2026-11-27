import argparse

from .llmconnection import run_agent_loop
from .logger import Event, Logger


def main() -> str:
    run_logger = Logger()

    try:
        parser = argparse.ArgumentParser()

        #Get arument and log beginning of the run

        parser.add_argument("value")
        args = parser.parse_args()
        run_logger.log_event(Event.USER_TASK, args={"message": args.value})

        #call OpenAI API with request

        content = run_agent_loop(args.value, run_logger)

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
        return f"An error occurred while running the agent: \n\n{error}\n\n" \
        "For more details see " + run_logger.get_log_file_name()


if __name__ == "__main__":
    print(main())
