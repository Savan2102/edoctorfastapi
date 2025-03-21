from fastapi import APIRouter
from models.PrescriptionModel import Prescription
from controllers.PrescriptionController import (
    create_prescription, get_prescriptions_by_user, get_prescriptions_by_doctor,
    delete_prescription, generate_prescription_pdf
)

router = APIRouter()

@router.post("/prescription/")
async def add_prescription(prescription: Prescription):
    return await create_prescription(prescription)

@router.get("/prescriptions/user/{user_id}")
async def fetch_prescriptions_by_user(user_id: str):
    return await get_prescriptions_by_user(user_id)

@router.get("/prescriptions/doctor/{doctor_id}")
async def fetch_prescriptions_by_doctor(doctor_id: str):
    return await get_prescriptions_by_doctor(doctor_id)

@router.delete("/prescription/{prescription_id}")
async def remove_prescription(prescription_id: str):
    return await delete_prescription(prescription_id)

@router.get("/prescription/{prescription_id}/pdf")
async def get_prescription_pdf(prescription_id: str):
    return await generate_prescription_pdf(prescription_id)
