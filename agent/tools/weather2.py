import json
from datetime import date
from typing import Any, Dict
from urllib.parse import urlencode
from urllib.request import urlopen

from .tool import tool
from ..utils import utils


class weather2(tool):
    @property
    def name(self) -> str:
        return "get_weather"

    @property
    def description(self) -> str:
        return "Retrieve weather data for one city and date."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "minLength": 1,
                    "description": "City to retrieve weather for.",
                },
                "date": {
                    "type": "string",
                    "format": "date",
                    "description": "Date, in YYYY-MM-DD format.",
                },
            },
            "required": ["city", "date"],
            "additionalProperties": False,
        }

    def run(self, arguments_json: str) -> str:
        arguments = json.loads(arguments_json)

        #Parse city and date

        city = arguments["city"].strip()
        if not city:
            raise ValueError("City must not be empty")
        parsed_date = utils.parse_date(arguments["date"])

        #Get location for city -> open meteo needs lat / long

        geocoding_url = (
            "https://geocoding-api.open-meteo.com/v1/search?"
            + urlencode({"name": city, "count": 1, "language": "de", "format": "json"})
        )
        with urlopen(geocoding_url) as response:
            locations = json.loads(response.read().decode("utf-8"))

        results = locations.get("results")
        if not results:
            return json.dumps(f"No location found for {city}")

        #Get weather data

        location = results[0]
        api_base_url = (
            "https://archive-api.open-meteo.com/v1/archive" #Dates in the past
            if parsed_date < date.today()
            else "https://api.open-meteo.com/v1/forecast" #Forecast
        )
        weather_url = api_base_url + "?" + urlencode(
            {
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "daily": "weather_code,temperature_2m_max,temperature_2m_min",
                "timezone": "auto",
                "start_date": parsed_date.isoformat(),
                "end_date": parsed_date.isoformat(),
            }
        )
        with urlopen(weather_url) as response:
            weather_data: Dict[str, Any] = json.loads(response.read().decode("utf-8"))

        return json.dumps(
            {
                "location": location.get("name", city),
                "country": location.get("country"),
                "weather": weather_data,
            }
        )
