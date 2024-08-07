import json
import ssl
import urllib.request
from dataclasses import dataclass
from json import JSONDecodeError
from urllib.error import URLError

import config
from exceptions import CantGetCoordinates


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    """Returns current coordinates using ip"""
    coordinates_response = _get_coordinates_by_ip_response()
    coordinates = _parse_coordinates_response(coordinates_response)

    return _round_coords(coordinates)


def _get_coordinates_by_ip_response() -> bytes:
    url = config.GPS_COORDS_URL
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise CantGetCoordinates


def _parse_coordinates_response(coordinates_response: bytes) -> Coordinates:
    try:
        coordinates_dict = json.loads(coordinates_response)
        latitude, longitude = map(
            _parse_float_coordinate, coordinates_dict["loc"].split(",")
        )
        return Coordinates(latitude=latitude, longitude=longitude)
    except (JSONDecodeError, KeyError):
        raise CantGetCoordinates


def _parse_float_coordinate(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise CantGetCoordinates


def _round_coords(coordinates: Coordinates) -> Coordinates:
    if not config.USE_ROUNDED_COORDS:
        return coordinates
    return Coordinates(
        *map(lambda c: round(c, 1), [coordinates.latitude, coordinates.longitude])
    )


if __name__ == "__main__":
    print(get_coordinates())
