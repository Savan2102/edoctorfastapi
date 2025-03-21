from config.database import prescription_collection
from models.PrescriptionModel import Prescription, PrescriptionOut
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime
import pdfkit
from bson.errors import InvalidId
pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")

# Create a new prescription
async def create_prescription(prescription: Prescription):
    prescription_data = prescription.dict()
    prescription_data["doctor_id"] = ObjectId(prescription_data["doctor_id"])
    prescription_data["user_id"] = ObjectId(prescription_data["user_id"])
    prescription_data["created_at"] = datetime.utcnow()

    result = await prescription_collection.insert_one(prescription_data)
    if result.inserted_id:
        return {"message": "Prescription created successfully"}
    raise HTTPException(status_code=400, detail="Failed to create prescription")


# Get prescriptions by user (patient)
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException

async def get_prescriptions_by_user(user_id: str):
    try:
        # Validate user_id
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid User ID format")

        prescriptions = await prescription_collection.find({"user_id": ObjectId(user_id)}).to_list(length=None)
        
        for prescription in prescriptions:
            prescription["id"] = str(prescription.pop("_id"))  # ✅ Rename `_id` to `id`
            prescription["doctor_id"] = str(prescription["doctor_id"])
            prescription["user_id"] = str(prescription["user_id"])

        return [PrescriptionOut(**prescription) for prescription in prescriptions]
    
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid User ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_prescriptions_by_doctor(doctor_id: str):
    try:
        # Validate if doctor_id is a valid ObjectId
        if not ObjectId.is_valid(doctor_id):
            raise HTTPException(status_code=400, detail="Invalid Doctor ID format")

        prescriptions = await prescription_collection.find({"doctor_id": ObjectId(doctor_id)}).to_list(length=None)

        for prescription in prescriptions:
            prescription["id"] = str(prescription.pop("_id"))  # ✅ Rename `_id` to `id`
            prescription["doctor_id"] = str(prescription["doctor_id"])
            prescription["user_id"] = str(prescription["user_id"])

        return [PrescriptionOut(**prescription) for prescription in prescriptions]
    
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Doctor ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete a prescription
async def delete_prescription(prescription_id: str):
    result = await prescription_collection.delete_one({"_id": ObjectId(prescription_id)})
    if result.deleted_count:
        return {"message": "Prescription deleted successfully"}
    raise HTTPException(status_code=400, detail="Failed to delete prescription")


# Generate a prescription PDF
import pdfkit
from bson import ObjectId
from fastapi import HTTPException

# Set correct path to wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

async def generate_prescription_pdf(prescription_id: str):
    try:
        # Validate prescription ID
        if not ObjectId.is_valid(prescription_id):
            raise HTTPException(status_code=400, detail="Invalid Prescription ID format")

        prescription = await prescription_collection.find_one({"_id": ObjectId(prescription_id)})
        if not prescription:
            raise HTTPException(status_code=404, detail="Prescription not found")

        html_content = f"""
        <html>
            <head><title>Prescription</title></head>
            <body>
                <h1>Prescription</h1>
                <p><strong>Doctor ID:</strong> {prescription["doctor_id"]}</p>
                <p><strong>Patient ID:</strong> {prescription["user_id"]}</p>
                <p><strong>Date:</strong> {prescription["created_at"]}</p>
                <h2>Medications:</h2>
                <ul>
                    {''.join([f'<li>{med["name"]} - {med["dosage"]} - {med["instructions"]}</li>' for med in prescription["medications"]])}
                </ul>
            </body>
        </html>
        """

        pdf_file_path = f"prescription_{prescription_id}.pdf"
        pdfkit.from_string(html_content, pdf_file_path, configuration=config)

        return {"message": "PDF generated successfully", "pdf_path": pdf_file_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
