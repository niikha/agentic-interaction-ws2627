import argparse

from .apicaller import call_groq_chat_completion


def main() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("value", help="String to pass to the agent")
    args = parser.parse_args()
    print(args.value)
    completion = call_groq_chat_completion(args.value)
    content = completion.choices[0].message.content
    if content is None or content.strip() == "":
        raise RuntimeError("The chat completion did not contain text content")
    return content


if __name__ == "__main__":
    print(main())
