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