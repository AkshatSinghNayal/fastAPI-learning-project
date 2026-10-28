from src.user.dtos import userSchema,loginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException,status,Request
from pwdlib import PasswordHash
from src.utils.settings import settings 
from src.utils.mail import send_email
from datetime import datetime, timedelta , timezone  # datetime gives me the current time , timedelta is used to add some time
import jwt 

PasswordHash = PasswordHash.recommended() # use of this is to create a password hash object that can be used to hash and verify passwords. The recommended() method returns an instance of the PasswordHash class that uses the recommended hashing algorithm (currently Argon2) and parameters for secure password hashing. This object can be used to hash passwords before storing them in the database and to verify passwords during login.

def get_password_hash(password): # This does not return the password in plain text, instead it returns a hashed version of the password which is more secure and can be stored in the database. This is done to ensure that even if the database is compromised, the passwords are not easily accessible to attackers.
    return PasswordHash.hash(password)

def verify_password(plain_password, hashed_password):
    return PasswordHash.verify(plain_password, hashed_password) # use of this is to verify that the plain text password provided by the user during login matches the hashed password stored in the database. The verify() method takes the plain text password and the hashed password as input and returns True if they match, and False otherwise. This is done to ensure that the user is authenticated and authorized to access the application.


async def register(body : userSchema , db : Session ):
    found = db.query(UserModel).filter(UserModel.username == body.username).first()
    if found:
        raise HTTPException(status_code=400, detail="Username already exists")

    found = db.query(UserModel).filter(UserModel.email == body.email).first() 
    if found:
        raise HTTPException(status_code=400, detail="Email already exists")


    user = UserModel(
        name = body.name,
        username=body.username,
        email=body.email,
        password=get_password_hash(body.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user) # refresh the user instance to get the updated data from the database, such as the auto-generated id.


    #send email to the user after registration
    res = await send_email([user.email]) 
    print(res)
    
     # print the response from the send_email function to the console. This is useful for debugging purposes, as it allows you to see if the email was sent successfully or if there were any errors. The response is a dictionary that contains a message indicating whether the email was sent successfully or not.

    
    # send_email function is called with a list containing the user's email address. This function is defined in the src/utils/mail.py file and is responsible for sending an email to the specified recipients. The email is sent asynchronously using FastAPI's background tasks, which allows the registration process to complete without waiting for the email to be sent.

    return {"message": "User registered successfully"}



def login_user( body : loginSchema , db : Session):
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not is_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="User Not Found can't login")

    if not verify_password(body.password, is_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid Password")

    exp_time = datetime.now(timezone.utc)+timedelta(minutes=settings.EXP_TIME)
    sub = {
        "_id" : is_user.id,
        "username" : is_user.username,
        "exp" : exp_time
    }

    token = jwt.encode(sub, settings.SECRET_KEY, settings.ALGORITHM)

    return {
        "token" : token
    } # token send thing is compulsury 



def is_authenticated(request : Request , db : Session):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Token is missing")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
         # payload is a dictionary that contains the data that was encoded in the token. In this case, it contains the user's id, username, and the expiration time of the token. The jwt.decode() function takes the token, the secret key, and the algorithm used to encode the token as arguments and returns the decoded payload. If the token is invalid or has expired, it will raise a jwt.PyJWTError exception.

        user_id = payload.get("_id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Token is invalid")
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="User not found")

        return user 
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Token has expired")
        
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Token is invalid") 
    
    
    
    # how to send token or get token ? : to get token we need to send a request to the login endpoint with the username and password in the body of the request. If the credentials are valid, the server will respond with a JSON object containing the token. The client can then store this token (usually in local storage or cookies) and include it in the Authorization header of subsequent requests to protected endpoints.

  