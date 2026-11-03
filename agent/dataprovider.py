import os
from datetime import date, timedelta
from urllib.error import HTTPError
from urllib.request import urlopen

from dotenv import load_dotenv

load_dotenv()

DATA_BASE_URL = os.environ["DATA_BASE_URL"]
CALENDAR_START_DATE = date(2026, 10, 26)
CALENDAR_END_DATE = date(2026, 11, 8)


def get_calendar_entries(start_date: str, end_date: str) -> list[str]:
    start = _parse_calendar_date(start_date)
    end = _parse_calendar_date(end_date)

    if start > end:
        raise ValueError("start_date must be on or before end_date")
    if start < CALENDAR_START_DATE or end > CALENDAR_END_DATE:
        raise ValueError(
            "Requested dates must be between "
            f"{CALENDAR_START_DATE.isoformat()} and {CALENDAR_END_DATE.isoformat()}"
        )

    entries = []
    current_date = start

    while current_date <= end:
        current_date_string = current_date.isoformat()
        url = f"{DATA_BASE_URL.rstrip('/')}/calendar/{current_date_string}.json"

        try:
            with urlopen(url) as response:
                entries.append(response.read().decode("utf-8"))
        except HTTPError as error:
            if error.code != 404:
                raise
            entries.append(f"No data available for {current_date_string}")
        current_date += timedelta(days=1)

    return entries


def _parse_calendar_date(value: str) -> date:
    parsed_date = date.fromisoformat(value)
    if parsed_date.isoformat() != value:
        raise ValueError(f"Date must use YYYY-MM-DD format: {value}")
    return parsed_date
