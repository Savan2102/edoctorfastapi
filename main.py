from fastapi import FastAPI
from routes.RoleRoutes import router as role_router
from routes.UserRoutes import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from routes.DoctorRoutes import router as doctor_router
from routes.AdminRoutes import router as admin_router
from routes.AppointmentRoutes import router as appointment_router
from routes.PrescriptionRoutes import router as prescription_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or a list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(role_router)
app.include_router(user_router)
app.include_router(doctor_router)
app.include_router(admin_router)
app.include_router(appointment_router)
app.include_router(prescription_router)


#routes


# #http://localhost:8000/test
# #get api...
# @app.get("/test/")
# async def test():
#     return "Hello"

# @app.get("/users/")
# async def getAllUsers():
#     return {"message":"Users fatched successfully!!","users":["ram","shyam","seeta","geeta"]}


# @app.get("/user/{userId}")
# async def getUserById(userId:str):
#     return {"messafe":f"user found with id {userId}"}
#     #return  {"message":"user found with id "+userId}

