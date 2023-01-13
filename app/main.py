import psycopg2
from typing import Optional,List
from fastapi import  FastAPI, Response, status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas
from .database import  engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

while True:
    try:
        conn=psycopg2.connect(host="localhost",database="blogApiFastApi",user="postgres",password="basseT_2000",cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("database connection was successfull ✅")
        break
    except Exception as error:
        print("connection to database was failed")
        print("error was ",error)
        time.sleep(3)

my_posts=[{"title":"title 1","content":"content 1","id":1},{"title":"title 2","content":"content 2","id":2},{"title":"title 3","content":"content 3","id":3}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p ['id'] == id:
            return i 

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
async def test_myposts(db: Session = Depends(get_db)):

    posts=db.query(models.Post).all()
    return {"data":posts}

@app.get("/posts",response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):

    posts=db.query(models.Post).all()
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db)):

    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    
@app.get("/posts/{id}",response_model=schemas.Post)
async def get_post(id:int,db: Session = Depends(get_db)):

    post= db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} was not found")
    return post

@app.delete("/posts/{id}")
async def delete_post(id:int,db: Session = Depends(get_db)):

    post= db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model=schemas.Post)
async def update_post(id:int,updated_post:schemas.PostCreate,db: Session = Depends(get_db)):
    
    post_query= db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()

    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} was not found")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()

@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):

    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
