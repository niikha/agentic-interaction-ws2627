import json
import os
from datetime import date
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen

from dotenv import load_dotenv

load_dotenv()

DATA_BASE_URL = os.environ["DATA_BASE_URL"]


class Utils:
    @staticmethod
    def normalize_city_name(value: str) -> str:
        normalized = value.lower().translate(
            str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue"})
        )
        return quote(normalized, safe="")

    @staticmethod
    def parse_date(value: str) -> date:
        parsed_date = date.fromisoformat(value)
        if parsed_date.isoformat() != value:
            raise ValueError(f"Date must use YYYY-MM-DD format: {value}")
        return parsed_date

    @staticmethod
    def fetch_data_from_base_url(path: str, not_found_message: str) -> str:
        url = f"{DATA_BASE_URL.rstrip('/')}/{path.lstrip('/')}"

        try:
            with urlopen(url) as response:
                result = response.read().decode("utf-8")
        except HTTPError as error:
            if error.code != 404:
                raise
            result = not_found_message
        return json.dumps(result)
