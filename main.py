from fastapi import FastAPI
from src.utils.settings import settings
from src.utils.db import Base, engine
from src.tasks.router import task_routes
from src.user.router import user_routes

Base.metadata.create_all(bind=engine) #this is done to create the tables in the database based on the models defined in the application.

app = FastAPI(title="Blog API", description="A simple blog API built with FastAPI and SQLAlchemy", version="1.0.0")
app.include_router(task_routes)
app.include_router(user_routes) #this is done to include the user routes in the application. The user routes are defined in the src/user/router.py file and are included in the application using the include_router method of the FastAPI class. This allows the application to handle requests to the user routes and return appropriate responses.













# the command to run the server is uvicorn main:app --reload. The --reload flag is used to enable hot reloading, which means that the server will automatically restart whenever you make changes to the code. This is useful for development, as it allows you to see the changes you make to the code without having to manually restart the server each time.    