from pydantic import BaseModel

class TaskSchema(BaseModel):
    title: str
    description: str
    status: bool = False

    class Config:
        orm_mode = True