from typing import Optional, List
from pydantic import (
    BaseModel,
    Field,
    validator,
    root_validator,
)

class AddLocation(BaseModel):
    city: str = Field(...)
    latitude: float = Field(None)
    longitude: float = Field(None)
    state: str = Field(None)
    country: str = Field(None)

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
