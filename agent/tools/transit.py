import json
import os
from typing import Any, Dict
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen

from dotenv import load_dotenv

from ..utils import utils
from .tool import tool

load_dotenv()

DATA_BASE_URL = os.environ["DATA_BASE_URL"]


class transit(tool):
    @property
    def name(self) -> str:
        return "get_transit"

    @property
    def description(self) -> str:
        return "Retrieve train connections between two cities for one date."

    @property
    def parameters(self) -> Dict[str, Any]:
        city_description = (
            "City name. Provide the name in German."
        )
        return {
            "type": "object",
            "properties": {
                "from": {
                    "type": "string",
                    "minLength": 1,
                    "description": f"Departure {city_description}",
                },
                "to": {
                    "type": "string",
                    "minLength": 1,
                    "description": f"Destination {city_description}",
                },
                "date": {
                    "type": "string",
                    "format": "date",
                    "description": "Date, in YYYY-MM-DD format.",
                },
            },
            "required": ["from", "to", "date"],
            "additionalProperties": False,
        }

    def run(self, arguments_json: str) -> str:
        arguments = json.loads(arguments_json)
        return json.dumps(
            self._get_transit(
                arguments["from"],
                arguments["to"],
                arguments["date"],
            )
        )

    def _get_transit(self, from_city: str, to_city: str, value: str) -> str:
        if not from_city.strip():
            raise ValueError("Departure city must not be empty")
        if not to_city.strip():
            raise ValueError("Destination city must not be empty")

        from_city_name = utils.normalize_city_name(from_city.strip())
        to_city_name = utils.normalize_city_name(to_city.strip())
        parsed_date = utils.parse_date(value)
        date_string = parsed_date.isoformat()
        from_path = quote(from_city_name, safe="")
        to_path = quote(to_city_name, safe="")
        url = (
            f"{DATA_BASE_URL.rstrip('/')}/transit/"
            f"{from_path}/{to_path}/{date_string}.json"
        )

        try:
            with urlopen(url) as response:
                return response.read().decode("utf-8")
        except HTTPError as error:
            if error.code != 404:
                raise
            return (
                f"No train connections available from {from_city_name} "
                f"to {to_city_name} on {date_string}"
            )
