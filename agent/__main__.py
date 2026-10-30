import argparse


def run(value: str) -> None:
    print(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("value", help="String to pass to the agent")
    args = parser.parse_args()
    run(args.value)


if __name__ == "__main__":
    main()
