# FastAPI Converts Dictionary to JSON Automatically
# PUT/PATCH for update all/specific field

# To run it on server type this on the terminal
# uvicorn <filename>:<FastAPI Instance> --reload
# uvicorn <package>.<filename>:<FastAPI Instance> --reload

# alembic --help to see what are the available methods in alembic
# alembic <method> --help to see how to use alembic method
# alembic looks like a git where you can see history, push, etc. on databases
# to set-up alembic you should look at alembic.ini and alembic/env.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .routers import post, user, auth, vote

# Create tables specified in model.py
# models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI()

# origins = ["https://www.google.com", "https://www.youtube.com"]
origins = ["*"] # if you want any domain to be able to access the API

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect "variable" from other directories
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)

# Root path
@app.get("/")
def root():
    return {"Message": "FAST API TUTORIAL"}



