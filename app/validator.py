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
