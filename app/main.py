from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

# Initialize an empty list to store posts
my_posts = []

async def find_post(id):
    for post in my_posts: # Iterate over the posts in my_posts list
        if post['id'] == id: # Check if the current post's id matches the provided id
            return post # If there is a match, return the post

# Asynchronously find the index of a post with a specific ID
async def find_index_post(id):
    # Iterate over the list of posts using enumerate to access both the index and the post
    for i, post in enumerate(my_posts):
        if post['id'] == id: # Check if the 'id' of the current post matches the provided 'id'
            return post

# Define the structure of a post using the Post model
class Post(BaseModel):
    title: str
    content: str
    is_published: bool = False
    rating: Optional[int] = None

while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', password='Access', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful!')
        break
    except Exception as error:
        print('Connection to database failed')
        print('Error: ', error)
        time.sleep(1)


@app.get("/favicon.ico")
async def get_favicon():
    return {"favicon": "This is a custom favicon response"}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone() 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": post} 


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
   cursor.execute("""INSERT INTO posts(title, content, is_published) VALUES (%s, %s, %s)""",(post.title, post.content, post.is_published))
   conn.commit()
   cursor.execute("""SELECT * FROM posts WHERE id = (SELECT MAX(id) FROM posts)""")
   new_post = cursor.fetchone()
    
   return {"data": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
   
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, updated_post: Post):
    post = await find_post(id)  # Await the find_post function
    # If post is not found, raise an HTTP 404 exception
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    # Update the post with the provided values from updated_post
    post.update(updated_post.model_dump(exclude_unset=True))
    
    return {"data": post}  # Return a JSON response with the updated post

