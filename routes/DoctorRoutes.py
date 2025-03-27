# from fastapi import APIRouter,HTTPException
# from models.DoctorModel import Doctor,DoctorOut
# from controllers import DoctorController
# from bson import ObjectId   

# router = APIRouter()    
# @router.post("/doctor")
# async def post_doctor(doctor:Doctor):
#     return await DoctorController.addDoctor(doctor)

# @router.get("/doctors")
# async def get_All_doctors():
#     return await DoctorController.getAllDoctors()
from fastapi import APIRouter
from models.DoctorModel import Doctor
from controllers.DoctorController import addDoctor, getAllDoctors

router = APIRouter()

@router.post("/doctor/")
async def post_doctor(doctor: Doctor):
    return await addDoctor(doctor)

@router.get("/doctors/")
async def get_all_doctors():
    return await getAllDoctors()
