import json
import os
from typing import Any, Dict
from urllib.error import HTTPError
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
                    "description": "City to retrieve weather for. Provide the name in German.",
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
        city = arguments["city"]
        if not city.strip():
            raise ValueError("City must not be empty")

        city_path = utils.normalize_city_name(city.strip())
        parsed_date = utils.parse_date(arguments["date"])
        date_string = parsed_date.isoformat()
        url = f"{DATA_BASE_URL.rstrip('/')}/weather/{city_path}/{date_string}.json"

        try:
            with urlopen(url) as response:
                result = response.read().decode("utf-8")
        except HTTPError as error:
            if error.code != 404:
                raise
            result = f"No weather data available for {city.strip()} on {date_string}"
        return json.dumps(result)
