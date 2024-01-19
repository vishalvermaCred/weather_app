from os import getenv

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

APP_NAME = getenv("SERVICE_NAME")
ENV = getenv("ENV", "PRODUCTION").lower()

LOG_LEVEL = getenv("LOG_LEVEL", "DEBUG")

BASE_ROUTE = getenv("BASE_ROUTE")
SERVICE_NAME = getenv("SERVICE_NAME")

HEADERS = {"Content-Type": "application/json"}
REDIS = {"HOST": getenv("REDIS_HOST"), "PORT": getenv("REDIS_PORT")}

# DB CONFIGS
DB_CONFIGS = {
    "HOST": getenv("DB_HOST"),
    "PORT": getenv("DB_PORT"),
    "NAME": getenv(f"DB_NAME"),
    "PASSWORD": getenv("DB_PASSWORD"),
    "USER": getenv("DB_USER"),
}

# BASE URLS
WEATHER_SERVICE_BASE_URL = getenv("WEATHER_SERVICE_BASE_URL")
OPEN_WEATHER_API_BASE_URL = getenv("OPEN_WEATHER_API_BASE_URL")

# CONST PARAMS
OPEN_WEATHER_GEO_PARAMS = getenv("OPEN_WEATHER_GEO_PARAMS")
OPEN_WEATHER_API_PARAMS = getenv("OPEN_WEATHER_API_PARAMS")

# API KEYS
OPEN_WEATHER_API_KEY = getenv("OPEN_WEATHER_API_KEY")