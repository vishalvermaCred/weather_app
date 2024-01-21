# weather_app
The Weather App is a simple and intuitive application that provides real-time and historical weather forecasts for specified locations. It fetches weather data from a reliable external weather service, allowing users to access accurate and up-to-date information.

## SETUP - with Docker
### create .env file
copy all the data from .env.example to newly created .env

### Docker setup steps
1. Install and start the Dockers
2. In terminal, go to the project directory
3. run command
    ```bash
    docker build -t weather-app .
    ```
4. after successful docker image creation run next command
    ```bash
    docker compose up
    ```
5. Now follow the documentation

## SETUP - Local Setup

### DB-SETUP
1. start PostgreSQL server in local
2. start PG admin 4
3. Create the user - "weather_db_user"
4. create the DB - "weather_db
5. use password - "password"

### Create .env file
copy all the data from .env.example to newly created .env

### Create venv
```bash
python3.9 -m venv .venv
source .venv/bin/activate
```

### install all the requirements in venv
```bash
pip install -r requirements.txt --no-cache-dir
```

### start the server
```bash
uvicorn app.server:app --reload --port 9200
```

### Open the documentation after starting the server
1. http://localhost:9200/docs
2. http://localhost:9200/redocs


## Documentation

### POST /locations
#### Request Body
1. The request body should be in raw JSON format.
2. It should include the following parameters: <br />
    I. city (string): The name of the city for the location. <br />
   II. latitude (number): The latitude coordinate of the location. (optional) <br />
  III. longitude (number): The longitude coordinate of the location. (optional) <br />
   IV. state (string): The state or region of the location. (optional) <br />
    V. country (string): The country of the location. (optional)
4. For more accuracy provide state and country, if latitude and longitude are not available 

#### Sample Body
```bash
{
    "city": "Manali",
    "latitude": 32.2454608,
    "longitude": 77.1872926,
    "state": "Himachal Pradesh",
    "country": "INDIA"
}
```

#### Sample Response
```bash
{
    "data": "2ef72cae-1881-4d91-9f66-624228cca7ee",
    "message": "location added successfully",
    "success": true
}
```

#### CURL
```bash
curl --location 'http://localhost:9200/locations' \
--header 'Content-Type: application/json' \
--data '{
    "city": "Manali",
    "latitude": 32.2454608,
    "longitude": 77.1872926,
    "state": "Himachal Pradesh",
    "country": "INDIA"
}'
```


### GET /locations
#### Sample Response
```bash
{
    "data": [
        {
            "city": "manali",
            "country": "india",
            "latitude": "32.2454608",
            "location_id": "28efb9d7-4911-4c61-852c-b46fb926daed",
            "longitude": "77.1872926",
            "state": "himachal pradesh"
        },
        {
            "city": "shimla",
            "country": "india",
            "latitude": "31.1041526",
            "location_id": "2ef72cae-1881-4d91-9f66-624228cca7ee",
            "longitude": "77.1709729",
            "state": "himachal pradesh"
        }
    ],
    "message": "all locations fetched successfully",
    "success": true
}
```

#### CURL
```bash
curl --location 'http://localhost:9200/locations'
```


### GET /locations/<location_id>
#### Sample Response
```bash
{
    "data": [
        {
            "city": "indore",
            "country": "IN",
            "latitude": "22.7203616",
            "location_id": "16dac885-86dc-41d3-bedc-775a5703dc8e",
            "longitude": "75.8681996",
            "state": "Madhya Pradesh"
        }
    ],
    "message": "location fetched successfully",
    "success": true
}
```

#### CURL
```bash
curl --location 'http://localhost:9200/locations/16dac885-86dc-41d3-bedc-775a5703dc8e'
```


### PUT /locations/<location_id>
#### Sample Body
```bash
{
    "city": "Manali",
    "latitude": 32.2454608,
    "longitude": 77.1872926,
    "state": "Himachal Pradesh",
    "country": "INDIA"
}
```

#### Sample Response
```bash
{
    "data": "16dac885-86dc-41d3-bedc-775a5703dc8e",
    "message": "location updated successfully",
    "success": true
}
```

#### CURL
```bash
curl --location --request PUT 'http://localhost:9200/locations/16dac885-86dc-41d3-bedc-775a5703dc8e' \
--header 'Content-Type: application/json' \
--data '{
    "city": "indore"
}'
```


### DELETE /locations/<location_id>
#### Sample Response
```bash
{
    "message": "location deleted successfully",
    "success": true
}
```

#### CURL
```bash
curl --location --request DELETE 'http://localhost:9200/locations/bd2ef8c8-5662-4562-82be-dc04dc7c904b'
```


### GET /weather/<location_id>
#### Sample Response
```bash
{
    "data": 
    {
        "air_pressure": "1025 hPa",
        "city": "manali",
        "current_weather": "Clouds",
        "description": "scattered clouds",
        "feels_like_temperature": "-3°C",
        "humidity": "59%",
        "temperature": "0°C",
        "windspeed": "3.39 m/s"
    },
    "message": "forecast retrieved successfully",
    "success": true
}
```

#### CURL
```bash
curl --location 'http://localhost:9200/weather/28efb9d7-4911-4c61-852c-b46fb926daed'
```


### GET /history/<location_id>
#### Sample Response
```bash
{
    "data": 
    {
        "history_data": 
        [
            {
                "air_pressure": 1016,
                "current_weather": "Clouds",
                "description": "broken clouds",
                "feels_like_temperature": 22,
                "humidity": 46,
                "temperature": 22,
                "windspeed": 3
            }
        ],
        "summary": 
        {
            "air_pressure": 
            {
                "average": 1016.0,
                "max": 1016,
                "min": 1016
            },
            "humidity": 
            {
                "average": 46.0,
                "max": 46,
                "min": 46
            },
            "temperature": 
            {
                "average": 22.0,
                "max": 22,
                "min": 22
            },
            "windspeed": 
            {
                "average": 3.0,
                "max": 3,
                "min": 3
            }
        }
    },
    "message": "history retrieved successfully",
    "success": true
}
```

#### CURL
value of days can be 7 or 15 or 30 only
```bash
curl --location 'http://localhost:9200/history/16dac885-86dc-41d3-bedc-775a5703dc8e?days=7'
```
