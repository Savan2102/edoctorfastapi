from models.DoctorModel import Doctor,DoctorOut
from fastapi import APIRouter,HTTPException
from config.database import doctor_collection
from bson import ObjectId
from fastapi.responses import JSONResponse

async def addDoctor(doctor:Doctor):
    savedDoctor = await doctor_collection.insert_one(doctor.dict())
    return JSONResponse(status_code=201,content={"message":"Doctor Created Successfully!"})

async def getAllDoctors():
    doctors = await doctor_collection.find().to_list()
    return [DoctorOut(**doctor) for doctor in doctors]