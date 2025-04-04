from pydantic import BaseModel,Field,validator
from bson import ObjectId
from typing import Optional, Dict, Any,List

class Doctor(BaseModel):
    FirstName:str
    LastName:str
    Specialization:str
    Phone:str
    Email:str
    RegistrationDate:str
    role_id:str


class DoctorOut(Doctor):
    id:str = Field(alias="_id")


    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
# from pydantic import BaseModel, Field, validator, EmailStr
# from bson import ObjectId
# from typing import Optional


# class Doctor(BaseModel):
#     FirstName: str
#     LastName: str
#     Specialization: str
#     Phone: str
#     Email: EmailStr
#     RegistrationDate: str
#     role_id: str

#     @validator("role_id", pre=True, always=True)
#     def validate_role_id(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid role ID format")
#         return v


# class DoctorOut(Doctor):
#     id: str = Field(alias="_id")

#     @validator("id", pre=True, always=True)
#     def convert_objectId(cls, v):
#         if isinstance(v, ObjectId):
#             return str(v)
#         return v
