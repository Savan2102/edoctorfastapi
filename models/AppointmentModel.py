from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import Optional
from datetime import datetime

class Appointment(BaseModel):
    doctor_id: str
    user_id: str
    date: str
    time: str
    status: str = "pending"

    @validator("doctor_id", "user_id", pre=True, always=True)
    def convert_object_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

class AppointmentOut(Appointment):
    id: str = Field(alias="_id")

    @validator("id", pre=True, always=True)
    def convert_object_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
