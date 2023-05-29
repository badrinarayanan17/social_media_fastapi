
from fastapi import FastAPI
from .import models
from .database import engine
from .routers import auth, post, user,votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# models.Base.metadata.create_all(bind=engine)

# Path Operations

@app.get("/")   
def root():
    return {"data":"First experience with fastapi"}

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Including the router in main.py

app.include_router(post.router)
app.include_router(user.router)   
app.include_router(auth.router)
app.include_router(votes.router)



