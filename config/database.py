from motor.motor_asyncio import AsyncIOMotorClient

#db url
MONGO_URL = "mongodb://localhost:27017"
DATABASE_NAME ="25_internship_fast"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

role_collection = db["roles"]
user_collection = db["users"]
doctor_collection = db["doctors"]
admin_collection = db["admins"]
appointment_collection = db["appointments"]
prescription_collection = db["prescription"]