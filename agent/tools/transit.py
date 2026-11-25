import json
import os
from typing import Any, Dict
from urllib.error import HTTPError
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
        from_city = arguments["from"]
        to_city = arguments["to"]

        from_path = utils.normalize_city_name(from_city.strip())
        to_path = utils.normalize_city_name(to_city.strip())
        parsed_date = utils.parse_date(arguments["date"])
        date_string = parsed_date.isoformat()
        url = (
            f"{DATA_BASE_URL.rstrip('/')}/transit/"
            f"{from_path}/{to_path}/{date_string}.json"
        )

        try:
            with urlopen(url) as response:
                result = response.read().decode("utf-8")
        except HTTPError as error:
            if error.code != 404:
                raise
            result = (
                f"No data for train connections available from {from_city.strip()} "
                f"to {to_city.strip()} on {date_string}"
            )
        return json.dumps(result)
