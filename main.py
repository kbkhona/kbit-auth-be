from fastapi import FastAPI, Depends, HTTPException
from model import User, Discussion
from app.handlers.register_handler import create_new_user
from app.handlers.login_handler import login_user
from app.auth.jwtBearer import jwtBearer
# from app.auth.jwt_handler import verify_jwt
from app.handlers.get_words_handler import random_word_generator
from app.database import save_discussion, get_discussions, logout_user


app = FastAPI()


# root
@app.get('/')
async def root():
    return {"message":"Welcome to Kibibit"}

# register endpoint
@app.post('/register')
async def register_user(user: User):
    return create_new_user(dict(user))

# login endpoint
@app.post('/login')
async def login(user: User):
    return login_user(dict(user))

# logout endpoint
@app.get('/logout', dependencies=[Depends(jwtBearer())])
async def logout(username: str):
    if not username:
        raise HTTPException(status_code=401, detail='logout unsuccessfull')
    logout_user(username)
    return {'message': 'logout successful'}

# get random text endpoint
@app.get('/get-random-text', dependencies=[Depends(jwtBearer())])
async def get_random_text():
    return {"random_words": random_word_generator()}

# get all discussions endpoint
@app.get('/get-all-discussions', dependencies=[Depends(jwtBearer())])
async def get_all_discussions():
    # print('token here',token)
    return get_discussions()

# save discussion endpoint
@app.post('/save-summary', dependencies=[Depends(jwtBearer())])
async def store_discussion(discussion: Discussion):
    return save_discussion(dict(discussion))
