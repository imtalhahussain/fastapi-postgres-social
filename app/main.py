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
from app.database import engine, SessionLocal, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.get("/posts", response_model= List[schemas.Post])
def get_post(db: Session =  Depends(get_db)):
    #for regular raw sql
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

# Adding a new post in the posts list (my_posts)
@app.post("/createposts", status_code=201, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute(
    #"""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #(post.title, post.content, post.published))
    #new_post= cursor.fetchall
    #conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Getting a specific post by id
@app.get("/posts/{id}", response_model= schemas.Post)
def get_post(id : int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE (id) = %s""",(str(id),))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail= f"Post {id} not found")
    return post

@app.delete("/posts/{id}",status_code=204)
def delete_post(id : int, db: Session = Depends(get_db)):
    #cursor.execute("""DELETE FROM posts WHERE(id) = %s returning *""",(str(id)),)
    #post_delete = cursor.fetchone()
    #conn.commit()
    post_delete = db.query(models.Post).filter(models.Post.id == id)
    if post_delete.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post {id} does not exist")
    post_delete.delete(synchronize_session=False)
    db.commit()                        
    return Response(status_code=204)

@app.put("/posts/{id}",response_model= schemas.Post)
def update_post(id : int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute(""" UPDATE posts SET title= %s, content= %s, published=%s WHERE id = %s RETURNING *""",(post.title, post.content, post.published,str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit() 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session= False)
    db.commit()
    return {"data" : post_query.first()}                         
