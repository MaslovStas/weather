from datetime import datetime

from weather_api_service import Weather, WeatherType


def format_weather(weather: Weather) -> str:
    """Formats weather data in string"""
    return (
        f"{weather.city}, температура {weather.temperature} °C, "
        f"{weather.weather_type.value}\n"
        f"Восход: {weather.sunrise.strftime('%H:%M')}\n"
        f"Закат: {weather.sunset.strftime('%H:%M')}\n"
    )


if __name__ == "__main__":
    print(
        format_weather(
            Weather(
                temperature=23,
                weather_type=WeatherType.CLEAR,
                sunrise=datetime.fromisoformat("2024-12-12 05:00:00"),
                sunset=datetime.fromisoformat("2024-12-12 21:00:00"),
                city="Liman",
            )
        )
    )
