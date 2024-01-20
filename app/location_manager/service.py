import json
import aiohttp
from uuid import uuid4
from http import HTTPStatus
from datetime import datetime
from quart import current_app as app

from ..constants import Tables
from app.settings import (
    OPEN_WEATHER_API_KEY,
    OPEN_WEATHER_API_BASE_URL,
    OPEN_WEATHER_GEO_PARAMS
)

LOGGER_KEY = "app.location_manager.service"

class locationManager:
    def __init__(self, kwargs: dict = {}) -> None:
        self.location_id = kwargs.get("location_id")
        self.city = kwargs.get("city")
        self.latitude = kwargs.get("latitude")
        self.longitude = kwargs.get("longitude")
        self.state = kwargs.get("state")
        self.country = kwargs.get("country")
    
    async def fetchLocations(self):
        """
        if location_id is provided then fetches that particular location otherwise
        fetches all locations
        """
        app.logger.info(f"{LOGGER_KEY}.fetchLocations")
        response = {"error": None, "data": [], "status_code": None}

        try:
            # check in cache 
            cached_location_data = None
            if self.location_id:
                cached_location_data = await app.redis.get(self.location_id)
            elif not self.location_id and not self.city:
                cached_location_data = await app.redis.get("all_locations")
            
            if cached_location_data:
                # cache hit
                app.logger.info(f"{LOGGER_KEY}.fetchLocations.cache_hit")
                response["data"] = cached_location_data
            else:
                # cache miss - get data from DB
                app.logger.info(f"{LOGGER_KEY}.fetchLocations.cache_miss")
                table_name = Tables.LOCATION.value.get("name")
                columns = Tables.LOCATION.value["get_columns"].copy()
                columns = ','.join(columns)
                where_clause = ""
                if self.location_id:
                    where_clause = f" WHERE location_id='{self.location_id}'"
                elif self.city:
                    where_clause = f" WHERE city='{self.city}'"
                
                select_query = f"SELECT {columns} FROM {table_name}{where_clause};"
                locations_data = await app.db.execute_raw_select_query(select_query)

                # set the data in redis
                if locations_data:
                    response["data"] = locations_data
                    if self.location_id:
                        await app.redis.set(key=self.location_id, value=locations_data)
                    else:
                        await app.redis.set(key="all_locations", value=locations_data)
        except Exception as e:
            app.logger.error(f"{LOGGER_KEY}.fetchLocations.exception: {str(e)}")
            response["error"] = str(e)
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        
        return response
    

    async def setLatLong(self):
        """
        Fetches lat long using openweather geo API
        """
        app.logger.info(f"{LOGGER_KEY}.setLatLong")
        response = {"error": None, "data": [], "status_code": None}
        try:
            url = f"{OPEN_WEATHER_API_BASE_URL}/{OPEN_WEATHER_GEO_PARAMS}"
            params = {
                "q": self.city,
                "appid": OPEN_WEATHER_API_KEY
            }
            app.logger.info(f"{LOGGER_KEY}.setLatLong.url: {url}")
            async with aiohttp.ClientSession() as client:
                geo_location_response = await client.get(url, params=params)
                status_code = geo_location_response.status
                response_text = await geo_location_response.text()
                response_text = json.loads(response_text)
                app.logger.info(f"{LOGGER_KEY}.setLatLong.status_code: {status_code}")
                if status_code != HTTPStatus.OK.value:
                    # api failure handled
                    app.logger.error(f"{LOGGER_KEY}.setLatLong.error: {response_text}")
                    response["error"] = response_text["message"]
                    response["status_code"] = HTTPStatus.FAILED_DEPENDENCY.value
                else:
                    # set the object data
                    self.latitude = response_text[0].get("lat")
                    self.longitude = response_text[0].get("lon")
                    self.state = response_text[0].get("state")
                    self.country = response_text[0].get("country")
        except Exception as e:
            app.logger.error(f"{LOGGER_KEY}.setLatLong.exception: {str(e)}")
            response["error"] = str(e)
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        
        return response
    

    async def addLocation(self):
        """
        add new location
        """
        app.logger.info(f"{LOGGER_KEY}.addLocation")
        response = {"error": None, "data": [], "status_code": None}

        try:
            # get the latitude and longitude if not provided
            if not (self.latitude and self.longitude):
                set_lat_long_response = await self.setLatLong()
                if set_lat_long_response.get("error"):
                    return set_lat_long_response

            # create a new location_id
            self.location_id = uuid4()
            table_name = Tables.LOCATION.value.get("name")
            columns = Tables.LOCATION.value["insert_columns"].copy()
            columns = ",".join(columns)

            # query to insert the location
            query = f"INSERT INTO {table_name} ({columns}) VALUES ('{self.location_id}', '{self.city}', {self.latitude}, {self.longitude}"
            query += f",'{self.state}'" if self.state else f", null"
            query += f",'{self.country}'" if self.country else f", null"
            query += f",'{datetime.now()}'"
            query += f",'{datetime.now()}');"

            insert_response = await app.db.execute_insert_or_update_query(query)
            app.logger.info(f"{LOGGER_KEY}.addLocation.insert_response: {insert_response}")
            response["data"] = self.location_id
            # delete the cache
            await app.redis.delete_without_pattern("all_locations")
        except Exception as e:
            app.logger.error(f"{LOGGER_KEY}.addLocation.exception: {str(e)}")
            response["error"] = str(e)
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        
        return response
    

    async def putLocation(self):
        """
        update already existing location
        """
        app.logger.info(f"{LOGGER_KEY}.putLocation")
        response = {"error": None, "data": [], "status_code": None}

        try:
            # get the latitude and longitude if not provided
            if not (self.latitude and self.longitude):
                set_lat_long_response = await self.setLatLong()
                if set_lat_long_response.get("error"):
                    return set_lat_long_response

            table_name = Tables.LOCATION.value.get("name")
            columns = Tables.LOCATION.value["insert_columns"].copy()
            columns.remove("created")
            columns = ",".join(columns)

            where_clause = f" WHERE location_id='{self.location_id}';"

            # query to put the new location
            query = f"UPDATE {table_name} SET city='{self.city}', latitude={self.latitude}, longitude={self.longitude}"
            query += f", state='{self.state}'" if self.state else f", null"
            query += f", country='{self.country}'" if self.country else f", null"
            query += f", updated='{datetime.now()}'"
            query += where_clause

            update_response = await app.db.execute_insert_or_update_query(query)
            app.logger.info(f"{LOGGER_KEY}.putLocation.update_response: {update_response}")
            response["data"] = self.location_id
            
            # delete the cache
            await app.redis.delete_without_pattern(self.location_id)
        except Exception as e:
            app.logger.error(f"{LOGGER_KEY}.putLocation.exception: {str(e)}")
            response["error"] = str(e)
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        
        return response
    

    async def deleteLocation(self):
        """
        delete the already existing location
        """
        app.logger.info(f"{LOGGER_KEY}.deleteLocation")
        response = {"error": None, "data": [], "status_code": None}

        try:
            table_name = Tables.LOCATION.value.get("name")
            query = f"DELETE FROM {table_name} WHERE location_id='{self.location_id}'"
            delete_response = await app.db.execute_insert_or_update_query(query)
            app.logger.info(f"{LOGGER_KEY}.deleteLocation.response: {delete_response}")
            response["data"] = self.location_id

            # delete the cache
            await app.redis.delete_without_pattern(self.location_id)
        except Exception as e:
            app.logger.error(f"{LOGGER_KEY}.deleteLocation.exception: {str(e)}")
            response["error"] = str(e)
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        
        return response
        
