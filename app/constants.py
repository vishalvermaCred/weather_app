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
        "get_columns": [
            "location_id::VARCHAR",
            "city",
            "latitude::VARCHAR",
            "longitude::VARCHAR",
            "state",
            "country",
        ],
        "insert_columns": [
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
        "get_columns": [
            "current_weather",
            "description",
            "temperature",
            "feels_like_temperature",
            "air_pressure",
            "humidity",
            "windspeed"
        ],
        "insert_columns": [
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