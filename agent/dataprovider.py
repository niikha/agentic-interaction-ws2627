import os
from datetime import date, timedelta
from urllib.error import HTTPError
from urllib.request import urlopen

from dotenv import load_dotenv

load_dotenv()

DATA_BASE_URL = os.environ["DATA_BASE_URL"]


def get_calendar_entries() -> list[str]:
    entries = []
    current_date = date(2026, 10, 26)
    end_date = date(2026, 11, 8)

    while current_date <= end_date:
        current_date_string = current_date.isoformat()
        url = f"{DATA_BASE_URL.rstrip('/')}/calendar/{current_date_string}.json"

        #Get calendar data for each day
        try:
            with urlopen(url) as response:
                entries.append(response.read().decode("utf-8"))

        #404 error: add "No data available" instead
        except HTTPError as error:
            if error.code != 404:
                raise
            entries.append(f"No data available for {current_date_string}")
        current_date += timedelta(days=1)

    return entries
