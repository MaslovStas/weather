import json
from datetime import datetime
from pathlib import Path
from typing import Protocol, TypedDict

from weather_api_service import Weather
from weather_formatter import format_weather


class WeatherStorage(Protocol):
    """Interface for any storage weather"""

    def save(self, weather: Weather) -> None:
        raise NotImplementedError


class PlainFileWeatherStorage:
    """Store weather in plain text file"""

    def __init__(self, file: Path) -> None:
        self._file = file

    def save(self, weather: Weather) -> None:
        now = datetime.now()
        formatted_weather: str = format_weather(weather)
        with open(self._file, "a") as f:
            f.write(f"{now}\n{formatted_weather}\n")


class HistoryRecord(TypedDict):
    date: str
    weather: str


class JSONFileWeatherStorage:
    """Store weather in JSON file"""

    def __init__(self, jsonfile: Path) -> None:
        self._jsonfile = jsonfile
        self._init_storage()

    def save(self, weather: Weather) -> None:
        history = self._read_history()
        new_record = HistoryRecord(
            date=str(datetime.now()), weather=format_weather(weather)
        )
        history.append(new_record)
        self._write_history(history)

    def _init_storage(self) -> None:
        if not self._jsonfile.exists():
            self._jsonfile.write_text("[]")

    def _read_history(self) -> list[HistoryRecord]:
        with open(self._jsonfile, "r") as f:
            return json.load(f)

    def _write_history(self, history: list[HistoryRecord]) -> None:
        with open(self._jsonfile, "w") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)


def save_weather(weather: Weather, storage: WeatherStorage) -> None:
    storage.save(weather)
