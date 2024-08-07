import json
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from json import JSONDecodeError
from typing import TypeAlias, Literal
from urllib.error import URLError

import config
from exceptions import APIServiceError
from gps_coordinates import Coordinates

Celsius: TypeAlias = float


class WeatherType(str, Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморось"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    ATMOSPHERE = "Туман"
    CLOUDS = "Облачно"


@dataclass(slots=True, frozen=True)
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates) -> Weather:
    """Requests weather in OpenWeather API and returns it"""
    openweather_response = _get_openweather_response(
        latitude=coordinates.latitude, longitude=coordinates.longitude
    )
    weather = _parse_openweather_response(openweather_response)
    return weather


def _get_openweather_response(latitude: float, longitude: float) -> bytes:
    url = config.OPENWEATHER_URL.format(lat=latitude, lon=longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise APIServiceError


def _parse_openweather_response(openweather_response: bytes) -> Weather:
    try:
        weather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        raise APIServiceError
    return Weather(
        temperature=_parse_temperature(weather_dict),
        weather_type=_parse_weather_type(weather_dict),
        sunset=_parse_sun_time(weather_dict, "sunset"),
        sunrise=_parse_sun_time(weather_dict, "sunrise"),
        city=_parse_city(weather_dict),
    )


def _parse_temperature(weather_dict: dict) -> Celsius:
    return round(weather_dict["main"]["temp"])


def _parse_weather_type(weather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(weather_dict["weather"][0]["id"])
    except (IndexError, KeyError):
        raise APIServiceError
    weather_types = {
        "2": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.ATMOSPHERE,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS,
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise APIServiceError


def _parse_sun_time(
    weather_dict: dict, time: Literal["sunset"] | Literal["sunrise"]
) -> datetime:
    return datetime.fromtimestamp(weather_dict["sys"][time])


def _parse_city(weather_dict: dict) -> str:
    return weather_dict["name"]


if __name__ == '__main__':
    print(get_weather(Coordinates(latitude=37.5974, longitude=48.8)))
