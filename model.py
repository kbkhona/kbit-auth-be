from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class Discussion(BaseModel):
    summary: str

class User_Logins(BaseModel):
    username: str
    access_token: str