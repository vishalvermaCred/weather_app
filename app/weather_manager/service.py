import json
import aiohttp
from uuid import uuid4
from http import HTTPStatus
from datetime import datetime
from quart import current_app as app

from ..constants import Tables, UNIT, Units
from app.location_manager.service import locationManager
from app.settings import (
    OPEN_WEATHER_API_KEY,
    OPEN_WEATHER_API_BASE_URL,
    OPEN_WEATHER_API_PARAMS
)

LOGGER_KEY = "app.wealth_manager.service"

class weatherManager:
    def __init__(self, kwargs) -> None:
        self.weather_id = kwargs.get("weather_id")
        self.location_id = kwargs.get("location_id")
        self.current_weather = kwargs.get("current_weather")
        self.description = kwargs.get("description")
        self.temperature = kwargs.get("temperature")
        self.feels_like_temperature = kwargs.get("feels_like_temperature")
        self.air_pressure = kwargs.get("air_pressure")
        self.humidity = kwargs.get("humidity")
        self.windspeed = kwargs.get("windspeed")
        self.days = kwargs.get("days")
        self.location_manager = locationManager(kwargs)
    
    async def getWeatherData(self):
        """
        get weather details from cache or DB if time is under an hour
        """
        app.logger.info(f"{LOGGER_KEY}.getWeatherData")
        response = {"error": None, "data": [], "status_code": None}
        try:
            table_name = Tables.WEATHER.value["name"]
            columns = Tables.WEATHER.value["columns"].copy()
            columns.remove("created")
            columns.remove("updated")
            columns = ",".join(columns)

            query = f"SELECT {columns} FROM {table_name} where location_id='{self.location_id}' and now()-created <= INTERVAL '1 hour' order by created desc limit 1;"
            weather_data = await app.db.execute_raw_select_query(query)
            if weather_data:
                response["data"] = weather_data[0]
        except Exception as e:
            app.logger.error(f"{LOGGER_KEY}.getForecast.exception: {str(e)}")
            response["error"] = str(e)
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        
        return response
    

    def setWeatherData(self, weather_data):
        """
        populates the weather object
        """
        app.logger.info(f"{LOGGER_KEY}.setWeatherData")
        self.current_weather = weather_data.get("current_weather")
        self.description = weather_data.get("description")
        self.temperature = weather_data["temperature"]
        self.feels_like_temperature = weather_data["feels_like_temperature"]
        self.air_pressure = weather_data["air_pressure"]
        self.humidity = weather_data["humidity"]
        self.windspeed = weather_data["windspeed"]
    

    def setWeatherDataFromOpenWeather(self, weather_data):
        """
        populates the weather object from data received from Open weather API
        """
        app.logger.info(f"{LOGGER_KEY}.setWeatherDataFromOpenWeather")
        current_weather_details = weather_data.get("weather",[])
        if len(current_weather_details) > 0:
            current_weather_details = current_weather_details[0]
            self.current_weather = current_weather_details.get("main")
            self.description = current_weather_details.get("description")
        
        temperature_details = weather_data.get("main")
        self.temperature = round(temperature_details["temp"])
        self.feels_like_temperature = round(temperature_details["feels_like"])
        self.air_pressure = temperature_details["pressure"]
        self.humidity = temperature_details["humidity"]
        self.windspeed = weather_data["wind"]["speed"]


    async def getOpenWeatherData(self, location_details):
        """
        gets weather data from third party API
        """
        app.logger.info(f"{LOGGER_KEY}.getOpenWeatherData")
        response = {"error": None, "data": [], "status_code": None}

        try:
            url = f"{OPEN_WEATHER_API_BASE_URL}/{OPEN_WEATHER_API_PARAMS}"
            params = {
                "lat": float(location_details.get("latitude")),
                "lon": float(location_details.get("longitude")),
                "units": UNIT,
                "appid": OPEN_WEATHER_API_KEY
            }
            async with aiohttp.ClientSession() as client:
                api_response = await client.get(url, params=params)
                status_code = api_response.status
                response_text = await api_response.text()
                response_text = json.loads(response_text)
                app.logger.info(f"{LOGGER_KEY}.getOpenWeatherData.status_code: {status_code}")
                if status_code != HTTPStatus.OK.value:
                    app.logger.error(f"{LOGGER_KEY}.getOpenWeatherData.error: {response_text}")
                    response["error"] = response_text["message"]
                    response["status_code"] = HTTPStatus.FAILED_DEPENDENCY.value
                response["data"] = response_text
        except Exception as e:
            app.logger.error(f"{LOGGER_KEY}.getOpenWeatherData.exception: {str(e)}")
            response["error"] = str(e)
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        
        return response


    async def insertWeatherData(self):
        """
        insert weather data into DB
        """
        app.logger.info(f"{LOGGER_KEY}.insertWeatherData")
        response = {"error": None, "data": [], "status_code": None}
        try:
            if not self.weather_id:
                self.weather_id = uuid4()
            
            table_name = Tables.WEATHER.value["name"]
            columns = Tables.WEATHER.value["columns"]
            columns = ",".join(columns)
            query = f"INSERT INTO {table_name} ({columns}) VALUES ('{self.weather_id}', '{self.location_id}', '{self.current_weather}'"
            query += f", '{self.description}'" if self.description else ", null"
            query += f", {self.temperature}" if self.temperature else ", null"
            query += f", {self.feels_like_temperature}" if self.feels_like_temperature else ", null"
            query += f", {self.air_pressure}" if self.air_pressure else ", null"
            query += f", {self.humidity}" if self.humidity else ", null"
            query += f", {self.windspeed}" if self.windspeed else ", null"
            query += f", '{datetime.now()}'"
            query += f", '{datetime.now()}');"

            insert_response = await app.db.execute_insert_or_update_query(query)
            app.logger.info(f"{LOGGER_KEY}.insertWeatherData.insert_response: {insert_response}")
        except Exception as e:
            app.logger.error(f"{LOGGER_KEY}.insertWeatherData.exception: {str(e)}")
            response["error"] = str(e)
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        
        return response
    

    async def getRealTimeWeatherData(self, location_details):
        """
        get the real time weather data
        """
        app.logger.info(f"{LOGGER_KEY}.getRealTimeWeatherData")
        response = {"error": None, "data": [], "status_code": None}
        try:
            weather_data = await self.getOpenWeatherData(location_details)
            if weather_data.get("error"):
                return weather_data
            weather_data["data"]["city"] = location_details["city"]
            response["data"] = weather_data["data"]
        except Exception as e:
            app.logger.error(f"{LOGGER_KEY}.getRealTimeWeatherData.exception: {str(e)}")
            response["error"] = str(e)
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        
        return response


    async def getForecast(self):
        """
        get the forecast for searched location_id
        """
        app.logger.info(f"{LOGGER_KEY}.getForecast")
        response = {"error": None, "data": [], "status_code": None}

        try:
            location_data_response = await self.location_manager.fetchLocations()
            if location_data_response.get("error"):
                return location_data_response
            if not location_data_response.get("data"):
                response["error"] = "location does not exist"
                response["status_code"] = HTTPStatus.BAD_REQUEST.value
                return response
            location_details = location_data_response["data"][0]

            weather_data = await self.getWeatherData()
            if weather_data.get("error"):
                return weather_data
            weather_data = weather_data["data"]
            if weather_data:
                self.setWeatherData(weather_data)
            
            if not weather_data:
                weather_data_response = await self.getRealTimeWeatherData(location_details)
                if weather_data_response.get("error"):
                    return weather_data_response
                weather_data = weather_data_response["data"]
            
                self.setWeatherDataFromOpenWeather(weather_data)
                insert_response = await self.insertWeatherData()
                if insert_response.get("error"):
                    return insert_response
            
            weather_data_formatted = {
                "city": location_details.get("city"),
                "current_weather": f"{self.current_weather}",
                "description": self.description,
                "temperature": f"{self.temperature}{Units.TEMPERATURE.value}",
                "feels_like_temperature": f"{self.feels_like_temperature}{Units.TEMPERATURE.value}",
                "air_pressure": f"{self.air_pressure} {Units.AIR_PRESSURE.value}",
                "humidity": f"{self.humidity}{Units.HUMIDITY.value}",
                "windspeed": f"{self.windspeed} {Units.WINDSPEED.value}"
            }
            response["data"] = weather_data_formatted 
        except Exception as e:
            app.logger.error(f"{LOGGER_KEY}.getForecast.exception: {str(e)}")
            response["error"] = str(e)
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        
        return response


    async def getHistoricalWeatherData(self):
        """
        get the last 7 or 15 or 30 days data from DB
        """
        app.logger.info(f"{LOGGER_KEY}.getWeatherData")
        response = {"error": None, "data": [], "status_code": None}
        try:
            table_name = Tables.WEATHER.value["name"]
            columns = Tables.WEATHER.value["columns"].copy()
            columns.remove("weather_id")
            columns.remove("location_id")
            columns.remove("created")
            columns.remove("updated")
            columns = ",".join(columns)
            interval = f"{self.days} days"

            query = f"SELECT {columns} FROM {table_name} where location_id='{self.location_id}' and now()-created <= INTERVAL '{interval}';"
            weather_data = await app.db.execute_raw_select_query(query)
            response["data"] = weather_data
        except Exception as e:
            app.logger.error(f"{LOGGER_KEY}.getForecast.exception: {str(e)}")
            response["error"] = str(e)
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        return response

    def getAttributeSummary(self, attribute):
        attribute_summary = {
            "max": max(attribute),
            "min": min(attribute),
            "average": sum(attribute)/len(attribute)
        }
        return attribute_summary

    def getSummary(self, history_data):
        """
        drive the summary of out of the history data
        """
        app.logger.info(f"{LOGGER_KEY}.getSummary")
        temperature, air_pressure, humidity, windspeed = [],[],[],[]
        for weather_data in history_data:
            temperature.append(weather_data["temperature"])
            air_pressure.append(weather_data["air_pressure"])
            humidity.append(weather_data["humidity"])
            windspeed.append(weather_data["windspeed"])
        
        summary = {
            "temperature": self.getAttributeSummary(temperature),
            "air_pressure": self.getAttributeSummary(air_pressure),
            "humidity": self.getAttributeSummary(humidity),
            "windspeed": self.getAttributeSummary(windspeed),
        }
        return summary


    async def getHistory(self):
        """
        fetches the history of last 7 or 15 or 30 days
        """
        app.logger.info(f"{LOGGER_KEY}.getHistory")
        response = {"error": None, "data": [], "status_code": None}

        try:
            history_data = await self.getHistoricalWeatherData()
            if history_data.get("error"):
                return history_data
            if not history_data.get("data"):
                response["error"] = "No history data available"
                response["status_code"] = HTTPStatus.OK.value
            history_data = history_data["data"]
            summary_response = self.getSummary(history_data)
            response["data"] = {
                "history_data": history_data,
                "summary": summary_response
            }
        except Exception as e:
            app.logger.error(f"{LOGGER_KEY}.getHistory.exception: {str(e)}")
            response["error"] = str(e)
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        
        return response