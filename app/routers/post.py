from fastapi import Body, HTTPException, FastAPI, Response,status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, Oauth2
from ..database import get_db

router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
)

@router.get("/", response_model= List[schemas.PostResponse])
def get_post(db: Session =  Depends(get_db)):
    #for regular raw sql
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

# Adding a new post in the posts list (my_posts)
@router.post("/", status_code=201, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(Oauth2.get_current_user)):
    #cursor.execute(
    #"""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #(post.title, post.content, post.published))
    #new_post= cursor.fetchall
    #conn.commit()
    print(user_id)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Getting a specific post by id
@router.get("/{id}", response_model= schemas.PostResponse)
def get_post(id : int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE (id) = %s""",(str(id),))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail= f"Post {id} not found")
    return post

@router.delete("/{id}",status_code=204)
def delete_post(id : int, db: Session = Depends(get_db), user_id: int = Depends(Oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE(id) = %s returning *""",(str(id)),)
    #post_delete = cursor.fetchone()
    #conn.commit()
    post_delete = db.query(models.Post).filter(models.Post.id == id)
    if post_delete.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post {id} does not exist")
    post_delete.delete(synchronize_session=False)
    db.commit()                        
    return Response(status_code=204)

@router.put("/{id}",response_model= schemas.PostResponse)
def update_post(id : int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), user_id: int = Depends(Oauth2.get_current_user)):
    #cursor.execute(""" UPDATE posts SET title= %s, content= %s, published=%s WHERE id = %s RETURNING *""",(post.title, post.content, post.published,str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit() 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session= False)
    db.commit()
    return post                         

