GPS_COORDS_URL = "https://ipinfo.io/json"
USE_ROUNDED_COORDS = True

OPENWEATHER_API = "fe9e57e36998e974144fd168a29ece2f"
OPENWEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather?"
    "lat={lat}&lon={lon}&"
    "appid=" + OPENWEATHER_API + "&lang=ru&units=metric"
)
