from pydantic import BaseModel

class TaskSchema(BaseModel):
    title: str
    description: str
    status: bool = False

    class Config:
        from_attributes = True # This is used to tell Pydantic that the model can be created from an ORM object. This is useful when we want to return the model as a response from the API endpoint, as it allows Pydantic to automatically convert the ORM object to a Pydantic model.


class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    status: bool = False

    class Config:
        from_attributes = True