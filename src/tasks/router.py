from src.tasks import controller
from src.utils.db import get_db
from fastapi import APIRouter,Depends,status
from src.tasks.dtos import TaskSchema
task_routes = APIRouter(prefix="/tasks")

@task_routes.post("/create",status_code=status.HTTP_201_CREATED) #the status_code parameter is used to set the status code of the response. In this case, it is set to 201, which means that the request was successful and a new resource was created.

def create_task(body : TaskSchema , db = Depends(get_db)):
    return controller.create_task(body,db) 

@task_routes.get("/getAll",status_code=status.HTTP_200_OK) #the status_code parameter is used to set the status code of the response. In this case, it is set to 200, which means that the request was successful and the response contains the requested data.

def get_tasks(db = Depends(get_db)):
    return controller.get_tasks(db) #why return because we are calling the get_tasks function from the controller and passing the db session to it. The get_tasks function will return a dictionary with the status and data of the tasks, which will be returned as the response of the API endpoint.

@task_routes.get("/getById/{id}")
def get_task_by_id(id : int , db = Depends(get_db)):
    return controller.get_task_by_id(id,db)

@task_routes.put("/update/{id}" , status_code=status.HTTP_201_CREATED) #the status_code parameter is used to set the status code of the response. In this case, it is set to 200, which means that the request was successful and the response contains the requested data.


def update_task( id:int , body : TaskSchema , db = Depends(get_db)):
    return controller.update_task(id,body,db)   

@task_routes.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT) #the status_code parameter is used to set the status code of the response. In this case, it is set to 204, which means that the request was successful and the response does not contain any content.

def delete_task(id:int , db = Depends(get_db)):
    return controller.delete_by_id(id,db)