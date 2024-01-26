from pymongo import MongoClient
from decouple import config
from fastapi import HTTPException

MONGO_USERNAME = config('MONGO_USERNAME')
MONGO_PASSWORD = config('MONGO_PASSWORD')

client = MongoClient(f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.vqmw9zo.mongodb.net/?retryWrites=true&w=majority")
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print('exception occured',e)

db = client.kibibit_db

users = db["user_collection"]
discussions = db["dicussions"]
user_logins = db["user_logins"]

def get_user(username) -> str:
    return list(users.find({"username": username}))

def save_discussion(summary):
    print(summary)
    try:
        discussions.insert_one(summary)
    except:
        return {}
    return { "message" : "Summary saved"}

def get_discussions():
    discussions_list: list[dict] = list(discussions.find())
    try:
        for discussion in discussions_list:
            discussion['_id'] = str(discussion['_id'])
    except:
        raise HTTPException(status_code=502, detail='could not fetch discussions')
    return discussions_list

def update_user_login(username:str, access_token:dict):
    filter_query = {"username": username}
    update_query = { "$set" : {**access_token} }
    try:        
        user_logins.update_one(filter_query, update_query, upsert=True)
    except:
        raise HTTPException(status_code=502, detail='could not update user logins')
    return True
    
def get_db_token(username: str) -> str:
    try:
        login_info = dict(user_logins.find_one({"username": username}))
    except:
        raise HTTPException(status_code=401, detail="UnAuthorised")
    return  login_info['access_token']

def logout_user(username: str):
    token = { "access_token": "" }
    if update_user_login(username, token):
        return {'message': 'logout successfull'}
    else:
        raise HTTPException(status_code=502, detail='could not logout user');