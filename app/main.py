from fastapi import Body, HTTPException, FastAPI, Response,status, Depends
from typing import Optional, List
from random import randrange
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from app import models
from app import schemas
from app import utils
from app.database import engine, SessionLocal, Base, get_db
from app.routers import post, user, auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

my_posts = [{"Title": "title of post 1", "Content": "content of post 1", "published": True, "Rating": 5, "id":1},{"Title": "title of post 2", "Content": "content of post 2", "published": False, "id":2}]
while True:
    try: 
        conn = psycopg2.connect(host='localhost', database='SMDB', user='postgres', password='password123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print ("DataBase Connection was Succesfull!")
        break
    except  Exception as error:
        print("Connecting to DataBase Failed")
        print("Error:", error)
        time.sleep(2)
        

# Finding a post by id
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def index_find_post(id):
    for i,p in enumerate(my_posts):
        if p ['id'] == id:
            return i

app.include_router(post.router)              
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

