from pydantic import BaseModel,Field,validator
from bson import ObjectId
from typing import Optional, Dict, Any,List

class Appointment(BaseModel):
    AppointmentID:str
    PatientID:str
    DoctorID:str
    AppointmentDate:str
    Reason:str
    Status:str


class AppointmentOut(Appointment):
    id:str = Field(alias="_id")

    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    
   
