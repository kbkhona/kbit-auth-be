from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import decodeJWT
from app.database import get_db_token

class jwtBearer(HTTPBearer) :
    def __init__(self, auto_Error : bool = True):
        super (jwtBearer, self).__init__(auto_error=auto_Error)
    
    async def __call__(self, request : Request):
        credentials: HTTPAuthorizationCredentials = await super (jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException (status_code = 403, details="Invalid or Expired Token!")
            print('credentials here', credentials.credentials)
            if verify_jwt(credentials.credentials):
                return credentials.credentials
            else: raise HTTPException(status_code = 403, details="hereInvalid or Expired Token!")
        else:
            raise HTTPException(status_code = 403, details="Invalid or Expired Token!")
    

def verify_jwt(jwtoken: str):
    isTokenValid : bool = False # A false flag
    payload = decodeJWT(jwtoken)
    print("jwtToken here", jwtoken)
    print("jwtdecoded username here", payload['username'])
    if payload and payload['username']:
        print('reached here')
        db_token = get_db_token(payload['username'])
        if db_token == jwtoken:
            print('db is valid')
            isTokenValid = True
        return isTokenValid
    else: raise HTTPException(status_code=401)