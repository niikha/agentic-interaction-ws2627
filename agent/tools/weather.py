import json
from typing import Any, Dict

from .tool import Tool
from ..utils import Utils


class Weather(Tool):
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
        city = arguments["city"].strip()
        if not city:
            raise ValueError("City must not be empty")

        city_path = Utils.normalize_city_name(city)
        date_string = arguments["date"]
        Utils.parse_date(date_string)
        return Utils.fetch_data_from_base_url(
            f"weather/{city_path}/{date_string}.json",
            f"No weather data available for {city} on {date_string}",
        )
