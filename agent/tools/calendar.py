import json
import os
from datetime import date
from typing import Any, Dict
from urllib.error import HTTPError
from urllib.request import urlopen

from dotenv import load_dotenv

from .tool import tool

load_dotenv()

DATA_BASE_URL = os.environ["DATA_BASE_URL"]


class calendar(tool):
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
        return json.dumps(self._get_calendar_entries(arguments["date"]))

    def _get_calendar_entries(self, value: str) -> str:
        parsed_date = self._parse_calendar_date(value)
        date_string = parsed_date.isoformat()
        url = f"{DATA_BASE_URL.rstrip('/')}/calendar/{date_string}.json"

        try:
            with urlopen(url) as response:
                return response.read().decode("utf-8")
        except HTTPError as error:
            if error.code != 404:
                raise
            return f"No data available for {date_string}"

    @staticmethod
    def _parse_calendar_date(value: str) -> date:
        parsed_date = date.fromisoformat(value)
        if parsed_date.isoformat() != value:
            raise ValueError(f"Date must use YYYY-MM-DD format: {value}")
        return parsed_date
