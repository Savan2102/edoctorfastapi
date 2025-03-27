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
from models.DoctorModel import Doctor, DoctorOut
from config.database import doctor_collection, role_collection
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi import HTTPException

async def addDoctor(doctor: Doctor):
    # Check if role_id is valid and belongs to a Doctor
    role = await role_collection.find_one({"_id": ObjectId(doctor.role_id)})

    if not role or role.get("name") != "Doctor":
        raise HTTPException(status_code=400, detail="Invalid role_id. Only users with 'Doctor' role can be created as doctors.")

    savedDoctor = await doctor_collection.insert_one(doctor.dict())
    return JSONResponse(status_code=201, content={"message": "Doctor Created Successfully!"})

async def getAllDoctors():
    doctors = await doctor_collection.find().to_list(length=None)
    return [DoctorOut(**doctor) for doctor in doctors]
# from config.database import doctor_collection
# from models.DoctorModel import Doctor, DoctorOut
# from bson import ObjectId
# from fastapi import HTTPException, UploadFile, File, Form
# from fastapi.responses import JSONResponse
# import shutil
# import os

# UPLOAD_DIR = "uploads/doctors/"  # Directory to store profile pictures
# os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure directory exists

# async def updateDoctorProfile(doctor_id: str, 
#                               FirstName: str = Form(...), 
#                               LastName: str = Form(...), 
#                               Specialization: str = Form(...), 
#                               Phone: str = Form(...), 
#                               Email: str = Form(...), 
#                               file: UploadFile = File(None)):

#     # Fetch doctor from DB
#     doctor = await doctor_collection.find_one({"_id": ObjectId(doctor_id)})
#     if not doctor:
#         raise HTTPException(status_code=404, detail="Doctor not found.")

#     update_data = {
#         "FirstName": FirstName,
#         "LastName": LastName,
#         "Specialization": Specialization,
#         "Phone": Phone,
#         "Email": Email
#     }

#     # Handle Profile Picture Upload
#     if file:
#         file_extension = file.filename.split(".")[-1]  # Get the file extension
#         file_path = os.path.join(UPLOAD_DIR, f"{doctor_id}.{file_extension}")

#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         update_data["ProfilePicture"] = f"/{file_path}"  # Store relative path for frontend use

#     # Update DB
#     await doctor_collection.update_one({"_id": ObjectId(doctor_id)}, {"$set": update_data})

#     # Fetch updated doctor profile
#     updated_doctor = await doctor_collection.find_one({"_id": ObjectId(doctor_id)})

#     return JSONResponse(status_code=200, content={
#         "message": "Doctor Profile Updated Successfully!",
#         "doctor": DoctorOut(**updated_doctor)  # Return updated data
#     })


# async def addDoctor(doctor: Doctor):
#     existing_doctor = await doctor_collection.find_one({"Email": doctor.Email})
#     if existing_doctor:
#         raise HTTPException(status_code=400, detail="Doctor with this email already exists.")
    
#     result = await doctor_collection.insert_one(doctor.dict())
#     return JSONResponse(status_code=201, content={"message": "Doctor Created Successfully!"})

# async def getDoctorById(doctor_id: str):
#     doctor = await doctor_collection.find_one({"_id": ObjectId(doctor_id)})
#     if not doctor:
#         raise HTTPException(status_code=404, detail="Doctor not found.")
#     return DoctorOut(**doctor)

# async def updateDoctorProfile(doctor_id: str, FirstName: str = Form(...), LastName: str = Form(...), 
#                               Specialization: str = Form(...), Phone: str = Form(...), 
#                               Email: str = Form(...), file: UploadFile = File(None)):
#     doctor = await doctor_collection.find_one({"_id": ObjectId(doctor_id)})
#     if not doctor:
#         raise HTTPException(status_code=404, detail="Doctor not found.")
    
#     update_data = {
#         "FirstName": FirstName,
#         "LastName": LastName,
#         "Specialization": Specialization,
#         "Phone": Phone,
#         "Email": Email
#     }

#     if file:
#         file_path = os.path.join(UPLOAD_DIR, f"{doctor_id}.jpg")
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
#         update_data["ProfilePicture"] = file_path  # Store image path in DB

#     await doctor_collection.update_one({"_id": ObjectId(doctor_id)}, {"$set": update_data})
#     return JSONResponse(status_code=200, content={"message": "Doctor Profile Updated Successfully!"})
