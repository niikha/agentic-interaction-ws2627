import json
from typing import Any, Dict

from ..utils import utils
from .tool import tool


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
        from_city = arguments["from"].strip()
        to_city = arguments["to"].strip()

        from_path = utils.normalize_city_name(from_city)
        to_path = utils.normalize_city_name(to_city)
        date_string = arguments["date"]
        utils.parse_date(date_string)
        return utils.fetch_data(
            f"transit/{from_path}/{to_path}/{date_string}.json",
            f"No data for train connections available from {from_city} "
            f"to {to_city} on {date_string}",
        )
