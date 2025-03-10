from pydantic import BaseModel,Field,validator
from bson import ObjectId
from typing import Optional, Dict, Any
import bcrypt   #pip install bcrypt

class Admin(BaseModel):
    firstName:str
    lastName:str
    admin_id:str
    email:str
    password:str
    
    #10,11,12,13,14,15,16,20,,,25,31
    @validator("password",pre=True,always=True)
    def encrypt_password(cls,v):
        if v is None:
            return None
        return bcrypt.hashpw(v.encode("utf-8"),bcrypt.gensalt())
        
    
    @validator("admin_id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    
class AdminOut(BaseModel):
    id:str = Field(alias="_id")    
    email:Optional[str] = None
    password:Optional[str] = None
    
    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    
class AdminLogin(BaseModel):
    email:str
    password:str