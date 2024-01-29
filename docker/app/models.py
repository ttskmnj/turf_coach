from pydantic import BaseModel, Field
from datetime import datetime


class Pitch(BaseModel):
    id: str = Field(alias='_id')
    name: str
    city: str
    state: str
    country: str
    type: int
    last_maintenace_date: datetime
    next_maintenace_date: datetime
    condition: int


class PitchCreate(BaseModel):
    name: str
    city: str
    state: str
    country: str
    type: int
    last_maintenace_date: datetime
    next_maintenace_date: datetime
    condition: int


class PitchUpdate(BaseModel):
    name: str
    type: int
    last_maintenace_date: datetime
    next_maintenace_date: datetime
    condition: int
