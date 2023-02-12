from typing import Optional,List
from fastapi import  FastAPI, Response, status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from . import models,schemas,utils
from .database import  engine,get_db
from sqlalchemy.orm import Session
from .routers import post,user,auth

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

my_posts=[{"title":"title 1","content":"content 1","id":1},{"title":"title 2","content":"content 2","id":2},{"title":"title 3","content":"content 3","id":3}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p ['id'] == id:
            return i 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
async def test_myposts(db: Session = Depends(get_db)):

    posts=db.query(models.Post).all()
    return {"data":posts}

