# Import the fastAPI class from the fastapi module
from fastapi import FastAPI

# Create an instance of the fastAPI class
app = FastAPI()


# Define an API endpoint for HTTP GET requests at the root URL '/'
# The function is asynchronous (async) and will be executed when the endpoint is requested
@app.get("/")
async def read_root():
    # Return a JSON response with the message {"Hello": "World"}
    return {"Hello": "World"}

@app.get("/post")
async def get_posts():
    return {"data": "This is posts data"}

# Define another API endpoint for HTTP GET requests at "/favicon.ico" URL
@app.get("/favicon.ico")
async def get_favicon():
    return {"favicon": "This is a custom favicon response"}