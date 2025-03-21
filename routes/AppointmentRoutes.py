from fastapi import APIRouter
from controllers.AppointmentController import (
    book_appointment,
    get_all_appointments,
    get_appointments_by_doctor,
    get_appointments_by_user,
    update_appointment_status,
    cancel_appointment,
)
from models.AppointmentModel import Appointment

router = APIRouter()

# Route to book an appointment
@router.post("/appointment/")
async def create_appointment(appointment: Appointment):
    return await book_appointment(appointment)


# Route to get all appointments
@router.get("/appointments/")
async def fetch_all_appointments():
    return await get_all_appointments()


# Route to get appointments by doctor ID
@router.get("/appointments/doctor/{doctor_id}")
async def fetch_appointments_by_doctor(doctor_id: str):
    return await get_appointments_by_doctor(doctor_id)


# Route to get appointments by user ID
@router.get("/appointments/user/{user_id}")
async def fetch_appointments_by_user(user_id: str):
    return await get_appointments_by_user(user_id)


# Route to update appointment status
@router.put("/appointment/{appointment_id}/status/{status}")
async def modify_appointment_status(appointment_id: str, status: str):
    return await update_appointment_status(appointment_id, status)


# Route to cancel an appointment
@router.delete("/appointment/{appointment_id}")
async def remove_appointment(appointment_id: str):
    return await cancel_appointment(appointment_id)
