# weather_app
The Weather App is a simple and intuitive application that provides real-time and historical weather forecasts for specified locations. It fetches weather data from a reliable external weather service, allowing users to access accurate and up-to-date information.

## SETUP

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
2. It should include the following parameters:
    city (string): The name of the city for the location.
    latitude (number): The latitude coordinate of the location. (optional)
    longitude (number): The longitude coordinate of the location. (optional)
    state (string): The state or region of the location. (optional)
    country (string): The country of the location. (optional)
3. For more accuracy provide state and country, if latitude and longitude are not available 

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