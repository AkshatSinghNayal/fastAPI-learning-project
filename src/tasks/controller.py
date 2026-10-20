from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel

def create_task(body: TaskSchema, db: Session):
    data = body.model_dump() #Convert the Pydantic model to a dictionary

    new_take = TaskModel(**data) #Create a new instance of the TaskModel using the data from the Pydantic model. The **data syntax is used to unpack the dictionary and pass its key-value pairs as keyword arguments to the TaskModel constructor. which simply means that the keys of the dictionary will be used as the names of the attributes of the TaskModel instance, and the values of the dictionary will be used as the values of those attributes.

    db.add(new_take) #Add the new instance of the TaskModel to the database session. This does not actually insert the data into the database yet, but it marks the instance as "pending" and prepares it to be inserted when the session is committed.
    
    db.refresh(new_take) # refresh the new instance of the TaskModel from the database. This is done to ensure that the instance has all of its attributes populated with the latest data from the database, including any default values or auto-generated values that may have been set by the database when the instance was added to the session.

    db.commit()#Commit the changes to the database. This actually inserts the new instance of the TaskModel into the database and makes the changes permanent.


    return {"message": "Task created successfully"}