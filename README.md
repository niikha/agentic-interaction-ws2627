# Calendar Agent

Calendar Agent answers prompts using daily calendar data and a Groq chat completion. It retrieves calendar JSON files for October 26 through November 8, 2026 and asks the configured model to answer using that information.

## Prerequisites

- Python 3.9 or later.
- Access to a Groq-compatible chat completion API and the calendar data endpoint.
- Install the project dependencies from the repository root:

  ```shell
  python -m pip install -r requirements.txt
  ```

- Create a `.env` file in the repository root with these variables:

  ```dotenv
  OPENAI_API_KEY=your_api_key
  OPENAI_BASE_URL=https://api.groq.com
  MODEL=your_model_id
  DATA_BASE_URL=https://your-calendar-data-host
  ```

  `OPENAI_API_KEY` authenticates with the chat completion API. `OPENAI_BASE_URL` is the API base URL passed to the Groq client; use the host/base URL without appending the chat-completions route. `MODEL` is the model identifier sent with the completion request. `DATA_BASE_URL` is the root URL for the calendar files, which are requested from `{DATA_BASE_URL}/calendar/YYYY-MM-DD.json`.

## Run

From the repository root, pass the prompt as a quoted command-line argument:

```shell
python -m agent "What is on the calendar?"
```

The program prints the model's response. If your `python` command uses another installation, run it with the Python environment where the dependencies are installed.
