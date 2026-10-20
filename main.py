from fastapi import FastAPI
from src.utils.settings import settings
from src.utils.db import Base, engine
from src.tasks.router import task_routes

Base.metadata.create_all(bind=engine) #this is done to create the tables in the database based on the models defined in the application.

app = FastAPI(title="Blog API", description="A simple blog API built with FastAPI and SQLAlchemy", version="1.0.0")
app.include_router(task_routes)