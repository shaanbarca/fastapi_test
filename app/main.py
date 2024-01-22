from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    database_password: str = "localhost"
    database_username: str = "postgres"
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# what if table DNE it creates new table

settings = Settings()
print("PASSWORD IS" + settings.database_password)
models.Base.metadata.create_all(bind=engine) # This creates table


app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# @app.get("/")
# def read_root():
#     return {"message": "welcome to the api"}

