from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from src.user.models import UserModel
from fastapi import HTTPException

def create_task(body: TaskSchema, db: Session , user: UserModel):
    data = body.model_dump() #Convert the Pydantic model to a dictionary
    data["user_id"] = user.id # Add the user's ID to the data dictionary

    new_take = TaskModel(**data) #Create a new instance of the TaskModel using the data from the Pydantic model. The **data syntax is used to unpack the dictionary and pass its key-value pairs as keyword arguments to the TaskModel constructor. which simply means that the keys of the dictionary will be used as the names of the attributes of the TaskModel instance, and the values of the dictionary will be used as the values of those attributes.

    db.add(new_take) #Add the new instance of the TaskModel to the database session. This does not actually insert the data into the database yet, but it marks the instance as "pending" and prepares it to be inserted when the session is committed.
    

    db.commit()#Commit the changes to the database. This actually inserts the new instance of the TaskModel into the database and makes the changes permanent.

    db.refresh(new_take) # refresh the new instance of the TaskModel from the database. This is done to ensure that the instance has all of its attributes populated with the latest data from the database, including any default values or auto-generated values that may have been set by the database when the instance was added to the session.

    return new_take 




def get_tasks(db: Session, user: UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()
    return tasks

def get_task_by_id( id : int , db : Session):
    task = db.query(TaskModel).filter(TaskModel.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def update_task(id: int, body: TaskSchema, db: Session , user: UserModel ):
    task = db.query(TaskModel).filter(TaskModel.id == id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    task.title = body.title
    task.description = body.description
    task.status = body.status

    
    db.commit()  
    db.refresh(task) 
    return task




def delete_by_id(id: int, db: Session, user : UserModel):
    task = db.query(TaskModel).filter(TaskModel.id == id).first()

    if task and task.user_id == user.id:
        db.delete(task)
        db.commit()
        return None
    else:
        raise HTTPException(status_code=404, detail="Task not found or not authorized to delete this task")
