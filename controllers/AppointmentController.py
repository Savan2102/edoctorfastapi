from models.AppointmentModel import Appointment,AppointmentOut
from fastapi import APIRouter
from bson import ObjectId
from config.database import appointment_collection
from fastapi.responses import JSONResponse


async def addAppointment(appointment:Appointment):
    savedAppointment = await appointment_collection.insert_one(appointment.dict())
    return JSONResponse(status_code=201,content={"message":"Appointment Created Successfully!"})

async def getAllAppointments():
    appointments = await appointment_collection.find().to_list()
    return [AppointmentOut(**appointment) for appointment in appointments]