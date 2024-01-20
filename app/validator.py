from typing import Optional, List
from pydantic import (
    BaseModel,
    Field,
    root_validator,
)

from app.constants import COUNTRY_CODES, STATE_NAME_TO_CODES

class AddLocation(BaseModel):
    city: str = Field(...)
    latitude: float = Field(None)
    longitude: float = Field(None)
    state: str = Field(None)
    country: str = Field(None)

    @root_validator(pre=True)
    def validator(cls, values):
        city = values.get("city")
        latitude = values.get("latitude")
        longitude = values.get("longitude")
        state = values.get("state")
        country = values.get("country")

        if city:
            values["city"] = city.lower()

        if latitude and not (isinstance(latitude, float) and (-90 <= latitude <= 90)):
            raise ValueError("wrong latitude")
        if longitude and not (isinstance(longitude, float) and (-180 <= longitude <= 180)):
            raise ValueError("wrong longitude")

        if state: 
            if not isinstance(state, str):
                raise ValueError("wrong state")
            else:
                state = state.lower()
                values["state"] = state
        
        if country:
            country = country.lower()
            if not (isinstance(country, str) and COUNTRY_CODES.get(country)):
                raise ValueError("wrong country")
            else:
                values["country"] = country
                if country == "india" and state and not STATE_NAME_TO_CODES.get(state):
                    raise ValueError("wrong state")
        
        return values


class PutLocation(BaseModel):
    city: str = Field(...)
    latitude: float = Field(None)
    longitude: float = Field(None)
    state: str = Field(None)
    country: str = Field(None)


class GetHistory(BaseModel):
    days: Optional[str] = None

    @root_validator(pre=True)
    def validator(cls, values):
        days = values.get("days")
        if days not in ['7','15','30']:
            raise ValueError("history of last 7, 15 and 30 days can be accessed")
        return values
