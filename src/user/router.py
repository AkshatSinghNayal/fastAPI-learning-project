from fastapi import APIRouter,Depends,status,Request
from src.user import controller
from src.user.dtos import userSchema,loginSchema,userResponseSchema
from sqlalchemy.orm import Session
from src.utils.db import get_db

user_routes = APIRouter(prefix="/user")

@user_routes.post("/register",status_code = status.HTTP_201_CREATED)
async def register_user( body : userSchema, db : Session = Depends(get_db)):
    return await controller.register(body,db)


@user_routes.post("/login",status_code=status.HTTP_200_OK)
def login( body : loginSchema , db : Session = Depends(get_db)):
    return controller.login_user(body , db)



@user_routes.get("/is_auth", response_model=userResponseSchema, status_code=status.HTTP_200_OK)
def is_auth(request : Request, db : Session = Depends(get_db)):
    return controller.is_authenticated(request,db)