from fastapi import Body, HTTPException, FastAPI, Response,status, Depends
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from app import models
from app.database import engine, SessionLocal, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #Rating: Optional[int] = None

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
              

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    return{'status': "Success"}

@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

# Adding a new post in the posts list (my_posts)
@app.post("/createposts", status_code=201)
def create_posts(post: Post):
    cursor.execute(
    """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

# Getting a specific post by id
@app.get("/posts/{id}")
def get_post(id : int):
    cursor.execute("""SELECT * FROM posts WHERE (id) = %s""",(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail= f"Post {id} not found")
    return {"post_detail": post}

@app.delete("/posts/{id}",status_code=204)
def delete_post(id : int):
    cursor.execute("""DELETE FROM posts WHERE(id) = %s returning *""",(str(id)),)
    post_delete = cursor.fetchone()
    conn.commit()
    if post_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post {id} does not exist")
                            
    return Response(status_code=204)

@app.put("/posts/{id}",)
def update_post(id : int, post: Post):
    cursor.execute(""" UPDATE posts SET title= %s, content= %s, published=%s WHERE id = %s RETURNING *""",(post.title, post.content, post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit() 
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post {id} does not exist")
    
    return {"data" : updated_post}                         
