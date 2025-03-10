from fastapi import APIRouter
from controllers import AppointmentController
from models.AppointmentModel import Appointment

router = APIRouter()

@router.post("/appointment")
async def post_appointment(appointment: Appointment):
    return await AppointmentController.addAppointment(appointment)

@router.get("/appointments")
async def get_all_appointments():
    return await AppointmentController.getAllAppointments()

