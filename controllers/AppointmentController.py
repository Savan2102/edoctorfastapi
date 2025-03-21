# from config.database import appointment_collection
# from models.AppointmentModel import Appointment, AppointmentOut
# from bson import ObjectId
# from fastapi import HTTPException


# # Book an appointment
# async def book_appointment(appointment: Appointment):
#     appointment_data = appointment.dict()
#     appointment_data["doctor_id"] = ObjectId(appointment_data["doctor_id"])
#     appointment_data["user_id"] = ObjectId(appointment_data["user_id"])

#     result = await appointment_collection.insert_one(appointment_data)
#     if result.inserted_id:
#         return {"message": "Appointment booked successfully"}
#     raise HTTPException(status_code=400, detail="Failed to book appointment")


# # Get all appointments
# async def get_all_appointments():
#     appointments = await appointment_collection.find().to_list(None)
    
#     for appointment in appointments:
#         appointment["_id"] = str(appointment.get("_id", ""))
#         appointment["doctor_id"] = str(appointment.get("doctor_id", ""))
#         appointment["user_id"] = str(appointment.get("user_id", ""))

#     return [AppointmentOut(**appointment) for appointment in appointments]


# # Get appointments by doctor ID
# async def get_appointments_by_doctor(doctor_id: str):
#     appointments = await appointment_collection.find({"doctor_id": ObjectId(doctor_id)}).to_list(length=None)
#     for appointment in appointments:
#         appointment["_id"] = str(appointment["_id"])
#         appointment["doctor_id"] = str(appointment["doctor_id"])
#         appointment["user_id"] = str(appointment["user_id"])
#     return [AppointmentOut(**appointment) for appointment in appointments]


# # Get appointments by user ID
# async def get_appointments_by_user(user_id: str):
#     appointments = await appointment_collection.find({"user_id": ObjectId(user_id)}).to_list(length=None)
#     for appointment in appointments:
#         appointment["_id"] = str(appointment["_id"])
#         appointment["doctor_id"] = str(appointment["doctor_id"])
#         appointment["user_id"] = str(appointment["user_id"])
#     return [AppointmentOut(**appointment) for appointment in appointments]


# # Update appointment status (e.g., confirmed, completed, canceled)
# async def update_appointment_status(appointment_id: str, status: str):
#     result = await appointment_collection.update_one(
#         {"_id": ObjectId(appointment_id)}, {"$set": {"status": status}}
#     )
#     if result.modified_count:
#         return {"message": "Appointment status updated successfully"}
#     raise HTTPException(status_code=400, detail="Failed to update appointment status")


# # Cancel an appointment
# async def cancel_appointment(appointment_id: str):
#     result = await appointment_collection.delete_one({"_id": ObjectId(appointment_id)})
#     if result.deleted_count:
#         return {"message": "Appointment canceled successfully"}
#     raise HTTPException(status_code=400, detail="Failed to cancel appointment")



from config.database import appointment_collection
from models.AppointmentModel import Appointment, AppointmentOut
from bson import ObjectId
from fastapi import HTTPException


# Book an appointment
async def book_appointment(appointment: Appointment):
    appointment_data = appointment.dict()

    try:
        appointment_data["doctor_id"] = ObjectId(appointment_data["doctor_id"])
        appointment_data["user_id"] = ObjectId(appointment_data["user_id"])
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid doctor_id or user_id format")

    result = await appointment_collection.insert_one(appointment_data)
    if result.inserted_id:
        return {"message": "Appointment booked successfully"}
    
    raise HTTPException(status_code=400, detail="Failed to book appointment")


# Get all appointments
async def get_all_appointments():
    try:
        # Fetch all appointments from MongoDB
        appointments = await appointment_collection.find().to_list(None)

        # Debugging: Print raw data from database
        print("Raw Appointments from DB:", appointments)

        # Convert ObjectId fields to string
        processed_appointments = []
        for appointment in appointments:
            processed_appointments.append({
                "_id": str(appointment.get("_id", "")),
                "doctor_id": str(appointment.get("doctor_id", "")),
                "user_id": str(appointment.get("user_id", "")),
                "date": appointment.get("date", ""),
                "time": appointment.get("time", ""),
                "status": appointment.get("status", "pending"),
            })

        # Debugging: Print processed appointments
        print("Processed Appointments:", processed_appointments)

        return processed_appointments  # Return JSON-friendly data

    except Exception as e:
        print("Error Fetching Appointments:", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch appointments")


# Get appointments by doctor ID
async def get_appointments_by_doctor(doctor_id: str):
    try:
        doctor_object_id = ObjectId(doctor_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid doctor_id format")

    appointments = await appointment_collection.find({"doctor_id": doctor_object_id}).to_list(None)

    for appointment in appointments:
        appointment["_id"] = str(appointment.get("_id", ""))
        appointment["doctor_id"] = str(appointment.get("doctor_id", ""))
        appointment["user_id"] = str(appointment.get("user_id", ""))

    return [AppointmentOut(**appointment) for appointment in appointments]


# Get appointments by user ID
async def get_appointments_by_user(user_id: str):
    try:
        user_object_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user_id format")

    appointments = await appointment_collection.find({"user_id": user_object_id}).to_list(None)

    for appointment in appointments:
        appointment["_id"] = str(appointment.get("_id", ""))
        appointment["doctor_id"] = str(appointment.get("doctor_id", ""))
        appointment["user_id"] = str(appointment.get("user_id", ""))

    return [AppointmentOut(**appointment) for appointment in appointments]


# Update appointment status (e.g., confirmed, completed, canceled)
async def update_appointment_status(appointment_id: str, status: str):
    try:
        appointment_object_id = ObjectId(appointment_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid appointment_id format")

    result = await appointment_collection.update_one(
        {"_id": appointment_object_id}, {"$set": {"status": status}}
    )
    if result.modified_count:
        return {"message": "Appointment status updated successfully"}

    raise HTTPException(status_code=400, detail="Failed to update appointment status")


# Cancel an appointment
async def cancel_appointment(appointment_id: str):
    try:
        appointment_object_id = ObjectId(appointment_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid appointment_id format")

    result = await appointment_collection.delete_one({"_id": appointment_object_id})

    if result.deleted_count:
        return {"message": "Appointment canceled successfully"}

    raise HTTPException(status_code=400, detail="Failed to cancel appointment")
