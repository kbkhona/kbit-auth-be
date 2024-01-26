from passlib.hash import pbkdf2_sha256
from fastapi import HTTPException
from model import User
from constants import db
from app.auth.jwt_handler import signJWT
from app.database import get_user, update_user_login

def verify_password(plainPwd: str, hashedPwd: str):
    return pbkdf2_sha256.verify(plainPwd, hashedPwd)


def login_user(user):    
    userInDb:list = get_user(user["username"])    
    if len(userInDb) < 1:
        raise HTTPException(status_code=400, detail='no user found')

    if not verify_password(user["password"], userInDb[0]["password"]):
        raise HTTPException(status_code=401)
    
    token = signJWT(userInDb[0]["username"])
    update_user_login(userInDb[0]["username"], token)
    return token

# def handle_user_logout(username):

# def authenticate_user(user:User):
#     print('check User model data fetch password',user["password"])
#     if (verify_password(user["password"], db["password"])):
    