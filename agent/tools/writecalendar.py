import json
from datetime import time
from pathlib import Path
from typing import Any, Dict

from ..utils import Utils
from .tool import Tool

CALENDAR_FILE = Path(__file__).resolve().parent.parent.parent / "var" / "calendar.jsonl"


def parse_time(value: str) -> time:
    parsed_time = time.fromisoformat(value)
    if parsed_time.strftime("%H:%M") != value:
        raise ValueError(f"Time must use HH:MM format: {value}")
    return parsed_time


class WriteCalendar(Tool):
    @property
    def name(self) -> str:
        return "write_calendar_entry"

    @property
    def description(self) -> str:
        return "Add an appointment to the calendar."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "format": "date",
                    "description": "Date of the appointment, in YYYY-MM-DD format.",
                },
                "start_time": {
                    "type": "string",
                    "description": "Start time of the appointment, in HH:MM format (24h).",
                },
                "end_time": {
                    "type": "string",
                    "description": "End time of the appointment, in HH:MM format (24h).",
                },
                "title": {
                    "type": "string",
                    "minLength": 1,
                    "description": "Title of the appointment.",
                },
            },
            "required": ["date", "start_time", "end_time", "title"],
            "additionalProperties": False,
        }

    def run(self, arguments_json: str) -> str:
        arguments = json.loads(arguments_json)

        date_string = arguments["date"]
        Utils.parse_date(date_string)
        start_time = arguments["start_time"]
        end_time = arguments["end_time"]
        if parse_time(end_time) <= parse_time(start_time):
            raise ValueError("End time must be after start time")
        title = arguments["title"].strip()
        if not title:
            raise ValueError("Title must not be empty")

        appointment = {
            "date": date_string,
            "start_time": start_time,
            "end_time": end_time,
            "title": title,
        }

        CALENDAR_FILE.parent.mkdir(parents=True, exist_ok=True)
        with CALENDAR_FILE.open("a", encoding="utf-8") as calendar_file:
            calendar_file.write(json.dumps(appointment, ensure_ascii=False) + "\n")

        return json.dumps({"status": "created", "appointment": appointment})
