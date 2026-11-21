# Calendar, Weather, and Transit Agent

The agent answers prompts using daily calendar, weather, and train connection data with an OpenAI chat completion. When this information is needed, the configured model calls the corresponding tool.

## Prerequisites

- Python 3.9 or later.
- Access to the OpenAI API with tool/function-calling support, and the calendar, weather, and transit data endpoints.
- Install the project dependencies from the repository root:

  ```shell
  python -m pip install -r requirements.txt
  ```

- Create a `.env` file in the repository root with these variables:

  ```dotenv
  OPENAI_API_KEY=your_api_key
  OPENAI_BASE_URL=https://api.openai.com/v1
  MODEL=your_model_id
  DATA_BASE_URL=https://your-data-host
  ```

  `OPENAI_API_KEY` authenticates with the OpenAI API. `OPENAI_BASE_URL` is the API base URL passed to the OpenAI client; use the host/base URL without appending the chat-completions route. `MODEL` is the model identifier sent with the completion request. `DATA_BASE_URL` is the root URL for the data files. Calendar files are requested from `{DATA_BASE_URL}/calendar/YYYY-MM-DD.json`; weather files are requested from `{DATA_BASE_URL}/weather/{city}/YYYY-MM-DD.json`; train connections are requested from `{DATA_BASE_URL}/transit/{from}/{to}/YYYY-MM-DD.json`.

## Run

From the repository root, pass the prompt as a quoted command-line argument:

```shell
python -m agent "What is on the calendar?"
```

The program prints the model's response. If your `python` command uses another installation, run it with the Python environment where the dependencies are installed.
