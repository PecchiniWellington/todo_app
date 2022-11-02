from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from .routes import user, auth, post, vote
from .config import settings

from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

print(settings.database_username)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)
