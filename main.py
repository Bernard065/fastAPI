# Import the fastAPI class from the fastapi module
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

# Create an instance of the fastAPI class
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
    is_published: bool = True
    rating: Optional[int] = None


# Define another API endpoint for HTTP GET requests at "/favicon.ico" URL
@app.get("/favicon.ico")
async def get_favicon():
    return {"favicon": "This is a custom favicon response"}

# Define an API endpoint for HTTP GET requests at the root URL '/'
# The function is asynchronous (async) and will be executed when the endpoint is requested
@app.get("/")
async def read_root():
    # Return a JSON response with the current list of posts
    return {"Hello": "World"}

# Define an API endpoint for HTTP POST requests at the '/posts' UR
@app.get("/posts")
async def get_posts():
    # Return a JSON response with the current list of post
    return {"data": my_posts}

# # Define an API endpoint for HTTP GET requests at the '/posts/{id}' URL
@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    post = await find_post(id) # Await the find_post function
    # If post is not found, raise an HTTP 404 exception
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": post} # Return a JSON response with the post


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(new_post: Post):
   # Convert new_post to a dictionary using .model_dump() method
   post_dict= new_post.model_dump()
   # Generate a random ID and add it to the post dictionary
   post_dict["id"] = randrange(0, 100000)
   # Append the post dictionary to the my_post list
   my_posts.append(post_dict)
   # Return a JSON response with the new post dictionary
   return {"data": post_dict}


# Define an API endpoint for HTTP DELETE requests at the '/posts/{id}' URL
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    # find the index in the array that has required ID
    post = await find_index_post(id)
    # checks if the post variable is None, indicating that a post with the provided ID was not found in the my_posts list.
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    my_posts.remove(post)
    return {"message": "Post was successfully created"}