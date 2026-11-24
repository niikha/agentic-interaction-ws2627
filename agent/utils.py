from datetime import date
from urllib.parse import quote


class utils:
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
