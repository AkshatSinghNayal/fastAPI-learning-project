from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from src.utils.settings import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # this is because we will be using the declarative system of sqlalchemy to define our models. The declarative system allows us to define our models as classes, which is more intuitive and easier to work with than the traditional way of defining models using tables and columns.

#models are defined as classes that inherit from the Base class. Each model class represents a table in the database, and each attribute of the class represents a column in the table. The Base class provides a number of methods and attributes that allow us to interact with the database, such as creating tables, querying data, and committing changes.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()