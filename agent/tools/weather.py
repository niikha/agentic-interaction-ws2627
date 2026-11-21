import json
import os
from typing import Any, Dict
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen

from dotenv import load_dotenv

from .tool import tool
from ..utils import utils

load_dotenv()

DATA_BASE_URL = os.environ["DATA_BASE_URL"]


class weather(tool):
    @property
    def name(self) -> str:
        return "get_weather"

    @property
    def description(self) -> str:
        return "Retrieve weather data for one city and date."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "minLength": 1,
                    "description": "City to retrieve weather for. Must be lowercase and in german with umlauts replaced.",
                },
                "date": {
                    "type": "string",
                    "format": "date",
                    "description": "Date, in YYYY-MM-DD format.",
                },
            },
            "required": ["city", "date"],
            "additionalProperties": False,
        }

    def run(self, arguments_json: str) -> str:
        arguments = json.loads(arguments_json)
        return json.dumps(
            self._get_weather(arguments["city"], arguments["date"])
        )

    def _get_weather(self, city: str, value: str) -> str:
        if not city.strip():
            raise ValueError("City must not be empty")

        parsed_date = utils.parse_date(value)
        date_string = parsed_date.isoformat()
        city_path = quote(city.strip(), safe="")
        url = f"{DATA_BASE_URL.rstrip('/')}/weather/{city_path}/{date_string}.json"

        try:
            with urlopen(url) as response:
                return response.read().decode("utf-8")
        except HTTPError as error:
            if error.code != 404:
                raise
            return f"No weather data available for {city.strip()} on {date_string}"
