from enum import Enum

UNIT = "metric"

class Units(Enum):
    TEMPERATURE = "°C"
    AIR_PRESSURE = "hPa"
    WINDSPEED = "m/s"
    HUMIDITY = "%"

class Tables(Enum):
    LOCATION = {
        "name": "locations",
        "columns": [
            "location_id",
            "city",
            "latitude",
            "longitude",
            "state",
            "country",
            "created",
            "updated"
        ]
    }

    WEATHER = {
        "name": "weather",
        "columns": [
            "weather_id",
            "location_id",
            "current_weather",
            "description",
            "temperature",
            "feels_like_temperature",
            "air_pressure",
            "humidity",
            "windspeed",
            "created",
            "updated"
        ]
    }