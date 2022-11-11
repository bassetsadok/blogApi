from typing import Optional
from fastapi import  FastAPI, Response, status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating:Optional[int]=None

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

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(post:Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": my_posts}
    
@app.get("/posts/{id}")
async def get_post(id:int):
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} was not found")
    return {"post":post}

@app.delete("/posts/{id}")
async def delete_post(id:int):
    index=find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id:int,post:Post):
    index=find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} was not found")
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    print(post)
    return {"message":"updated post"}
