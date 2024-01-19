CREATE TABLE locations (
    location_id UUID PRIMARY KEY,
    city VARCHAR(50) UNIQUE NOT NULL,
    latitude DECIMAL NOT NULL,
    longitude DECIMAL NOT NULL,
    state VARCHAR(50),
    country VARCHAR(50),
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE weather (
    weather_id UUID PRIMARY KEY,
    location_id UUID REFERENCES locations(location_id),
    current_weather VARCHAR(50),
    description VARCHAR(100),
    temperature INTEGER NOT NULL,
    feels_like_temperature INTEGER,
    air_pressure INTEGER,
    humidity INTEGER,
    windspeed INTEGER,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);