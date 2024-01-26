import time
from jose import jwt
from decouple import config
from fastapi import HTTPException


JWT_SECRET = config('SECRET_KEY')
JWT_ALGORITHM = config('ALGORITHM')
# TOKEN_EXPIRY = config('TOKEN_EXPIRY')

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(username : str) :
    payload = {
        "username" : username,
        "expiry" : time.time() + 600000
    }
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token : str):
    try:
        print('hello there')
        decode_token = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        print('decode token here', decode_token)
        return decode_token if decode_token['expiry'] >= time.time() else None 
    except:
        raise HTTPException(status_code='401', detail='jwt error')
    
# def verify_jwt(jwtoken:str = Depends(jwtBearer())):
#     isTokenValid : bool = False # A false flag
#     payload = decodeJWT(jwtoken)
#     print("jwtToken here", payload.get('username'))
#     if payload and payload['username']:
#         db_token = get_db_token(payload['username'])
#         if db_token == jwtoken:
#             isTokenValid = True
#     return isTokenValid