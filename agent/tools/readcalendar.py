import json
from typing import Any, Dict

from .tool import Tool
from ..utils import Utils


class ReadCalendar(Tool):
    @property
    def name(self) -> str:
        return "get_calendar_entries"

    @property
    def description(self) -> str:
        return "Retrieve calendar entries for one date."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "format": "date",
                    "description": "Calendar date, in YYYY-MM-DD format.",
                },
            },
            "required": ["date"],
            "additionalProperties": False,
        }

    def run(self, arguments_json: str) -> str:
        arguments = json.loads(arguments_json)
        date_string = arguments["date"]
        Utils.parse_date(date_string)
        return Utils.fetch_data_from_base_url(
            f"calendar/{date_string}.json",
            f"No data available for {date_string}",
        )
