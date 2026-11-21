from datetime import date


class utils:
    @staticmethod
    def normalize_city_name(value: str) -> str:
        return value.lower().translate(
            str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue"})
        )

    @staticmethod
    def parse_date(value: str) -> date:
        parsed_date = date.fromisoformat(value)
        if parsed_date.isoformat() != value:
            raise ValueError(f"Date must use YYYY-MM-DD format: {value}")
        return parsed_date
