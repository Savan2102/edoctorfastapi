from models.UserModel import User,UserOut,UserLogin,ResetPasswordReq
from bson import ObjectId
from config.database import user_collection,role_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import bcrypt
from utils.SendMail import send_mail
import datetime
import jwt

async def addUser(user: User):
    # Validate role_id
    role = await role_collection.find_one({"_id": ObjectId(user.role_id)})
    
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role_id. Please provide a valid role.")

    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user.password = hashed_password  # Store hashed password
    
    result = await user_collection.insert_one(user.dict())
    
    # Send email notification
    send_mail(user.email, "User Created", "User created successfully")
    
    return JSONResponse(status_code=201, content={"message": "User Created Successfully!"})
# async def addUser(user:User):
#     user.role_id = ObjectId(user.role_id)
#     print("after type cast",user.role_id)
#     result = await user_collection.insert_one(user.dict())
#     send_mail(user.email,"User Created","User created successfully")
#     # return {"message":"User Created Successfully!"}
#     return JSONResponse(status_code =201,content={"message":"User Created Successfully!"})
# # async def getAllUsers():
#     users = await user_collection.find().to_list()
#     print("users...",users)
#     return [UserOut(**user) for user in users]
# async def addUser(user:User):
#     result = await user_collection.insert_one(user.dict())
#     return{"message":"User create successfully..!"}

async def deleteUser(userId:str):
    result = await user_collection.delete_one({"_id":ObjectId(userId)})
    print("after delete result",result)
    return {"Message":"user Deleted Successfully!"}

async def getUserById(userId:str):
    result = await user_collection.find_one({"_id":ObjectId(userId)})
    print(result)        
    return UserOut(**result)

async def getAllUsers():
    users = await user_collection.find().to_list(length=None)

    for user in users:
            if "role_id" in user and isinstance(user["role_id"],ObjectId):
                    user["role_id"] = str(user["role_id"])

            role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})
            print("Role found:", role)#print role


            if role:
                role["_id"] = str(role["_id"])
                user["role"] = role

    return [UserOut(**user) for user in users]
        
        
# async def loginUser(request: UserLogin):
#     foundUser = await user_collection.find_one({"email": request.email})
#     print("found user",foundUser)
#     foundUser["_id"] = str (foundUser["_id"])
#     foundUser["role_id"] = str(foundUser["role_id"])

#     if foundUser is None:
#         raise HTTPException(status_code=404,detail="user not found")
    
# # for compare password
#     if "password" in foundUser and bcrypt.checkpw(request.password.encode(),foundUser["password"].encode()):
#         role = await role_collection.find_one({"_id":ObjectId(foundUser["role_id"])})
#         # foundUser["role"] = role
#         if role:
#             role["_id"] = str(role["_id"])  # Convert ObjectId to string for response
#             foundUser["role"] = role
#         else:
#             foundUser["role"] = None  # If role is not found, set it to None
#         return{"message":"user login successfully..!","user":UserOut(**foundUser)}
#     else:
#         raise HTTPException(status_code=404,detail="Invalid password")
    
async def loginUser(request: UserLogin):
    foundUser = await user_collection.find_one({"email": request.email})

    if not foundUser:
        raise HTTPException(status_code=404, detail="User not found")

    foundUser["_id"] = str(foundUser["_id"])
    foundUser["role_id"] = str(foundUser["role_id"])

    stored_password = foundUser["password"]  # Get stored password directly

    # Ensure stored_password is in string format before encoding
    if isinstance(stored_password, bytes):  # If already in bytes, use as is
        password_bytes = stored_password
    else:
        password_bytes = stored_password.encode("utf-8")  # Convert to bytes if string

    if bcrypt.checkpw(request.password.encode("utf-8"), password_bytes):
        role = await role_collection.find_one({"_id": ObjectId(foundUser["role_id"])})
        
        if role:
            role["_id"] = str(role["_id"])  
            foundUser["role"] = role
        else:
            foundUser["role"] = None  
        
        return {"message": "User login successful!", "user": UserOut(**foundUser)}
    else:
        raise HTTPException(status_code=401, detail="Invalid password")

    
SECRET_KEY ="royal"
def generate_token(email:str):
    expiration =datetime.datetime.utcnow()+datetime.timedelta(hours=1)
    payload = {"sub":email,"exp":expiration}
    token = jwt.encode(payload,SECRET_KEY,algorithm="HS256")
    return token


async def forgotPassword(email:str):
    foundUser = await user_collection.find_one({"email":email})
    if not foundUser:
        raise HTTPException(status_code=404,detail="email not found")
    
    token = generate_token(email)
    resetLink = f"http://localhost:5173/resetpassword/{token}"
    body = f"""
    <html>
        <h1>HELLO THIS IS RESET PASSWORD LINK EXPIRES IN 1 hour</h1>
        <a href= "{resetLink}">RESET PASSWORD</a>
    </html>
    """
    subject = "RESET PASSWORD"
    send_mail(email,subject,body)
    return {"message":"reset link sent successfully"}
    

async def resetPassword(data:ResetPasswordReq):
    try:
        payload =jwt.decode(data.token,SECRET_KEY,algorithms="HS256") #{"sub":"email...",exp:}
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=421,detail="token is not valid...")
        
        hashed_password = bcrypt.hashpw(data.password.encode('utf-8'),bcrypt.gensalt())
        await user_collection.update_one({"email":email},{"$set":{"password":hashed_password}})
        
        return {"message":"password updated successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=500,detail="jwt is expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=500,detail="jwt is invalid")    

# from config.database import user_collection, role_collection
# from models.UserModel import User, UserOut, UserLogin
# from bson import ObjectId
# from fastapi import HTTPException
# from fastapi.responses import JSONResponse
# import bcrypt
# from utils.SendMail import send_mail

# async def addUser(user: User):
#     # Check if user already exists
#     existing_user = await user_collection.find_one({"email": user.email})
#     if existing_user:
#         raise HTTPException(status_code=400, detail="User with this email already exists.")

#     user.role_id = ObjectId(user.role_id)
    
#     result = await user_collection.insert_one(user.dict())
#     send_mail(user.email, "User Created", "User created successfully")

#     return JSONResponse(status_code=201, content={"message": "User Created Successfully!"})

# async def deleteUser(userId: str):
#     if not ObjectId.is_valid(userId):
#         raise HTTPException(status_code=400, detail="Invalid user ID format.")

#     result = await user_collection.delete_one({"_id": ObjectId(userId)})
    
#     if result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="User not found.")

#     return {"message": "User Deleted Successfully!"}

# async def getUserById(userId: str):
#     if not ObjectId.is_valid(userId):
#         raise HTTPException(status_code=400, detail="Invalid user ID format.")

#     result = await user_collection.find_one({"_id": ObjectId(userId)})
    
#     if not result:
#         raise HTTPException(status_code=404, detail="User not found.")

#     return UserOut(**result)

# async def getAllUsers():
#     users = await user_collection.find().to_list(length=None)

#     if not users:
#         raise HTTPException(status_code=404, detail="No users found.")

#     for user in users:
#         if "role_id" in user and isinstance(user["role_id"], ObjectId):
#             user["role_id"] = str(user["role_id"])

#         role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})

#         if role:
#             role["_id"] = str(role["_id"])
#             user["role"] = role

#     return [UserOut(**user) for user in users]

# async def loginUser(request: UserLogin):
#     foundUser = await user_collection.find_one({"email": request.email})
    
#     if not foundUser:
#         raise HTTPException(status_code=404, detail="User not found.")

#     foundUser["_id"] = str(foundUser["_id"])
#     foundUser["role_id"] = str(foundUser["role_id"])

#     if bcrypt.checkpw(request.password.encode(), foundUser["password"].encode()):
#         role = await role_collection.find_one({"_id": ObjectId(foundUser["role_id"])})

#         if role:
#             role["_id"] = str(role["_id"])
#             foundUser["role"] = role
#         else:
#             foundUser["role"] = None

#         return {"message": "User login successful!", "user": UserOut(**foundUser)}
#     else:
#         raise HTTPException(status_code=401, detail="Invalid password")
