from passlib.hash import pbkdf2_sha256
from fastapi import HTTPException
from app.auth.jwt_handler import signJWT
from app.database import users, get_user, update_user_login

def create_hashed_password(password):
   return pbkdf2_sha256.hash(password)

def create_new_user(user):
   if get_user(user["username"]):
      print('user here',get_user(user["username"]))
      raise HTTPException(status_code=400, detail='username already exists')
 
   hashedPassword = create_hashed_password(user["password"])
   user["password"] = hashedPassword
   users.insert_one(user)
   access_token = signJWT(user["username"])   
   update_user_login(user["username"], access_token)
   return access_token



