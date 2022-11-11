import psycopg2
from typing import Optional
from fastapi import  FastAPI, Response, status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating:Optional[int]=None

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

@app.get("/posts")
async def get_posts():

    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()

    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(post:Post):

    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
                    (post.title,post.content,post.published))
    post=cursor.fetchone()
    conn.commit()

    return {"data": post}
    
@app.get("/posts/{id}")
async def get_post(id:int):

    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    post=cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} was not found")
    return {"post":post}

@app.delete("/posts/{id}")
async def delete_post(id:int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id:int,post:Post):

    cursor.execute("""UPDATE posts SET TITLE=%s, CONTENT=%s, PUBLISHED=%s WHERE ID=%s  RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()

    if updated_post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} was not found")
    return {"message":updated_post}
