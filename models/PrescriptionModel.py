from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Medication(BaseModel):
    name: str
    dosage: str
    instructions: str

class Prescription(BaseModel):
    doctor_id: str
    user_id: str
    medications: List[Medication]
    created_at: datetime = datetime.utcnow()

class PrescriptionOut(Prescription):
    id: str
