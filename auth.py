from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer


SECRECT_KEY = "key"
ALGO ="HS256"
ACCESS_TOKEN_EXPIRE = 30

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

def create_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE)

    to_encode.update({
        "exp":expire
    })
    return jwt.encode(to_encode,SECRECT_KEY,algorithm=ALGO)


def verify(token:str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, SECRECT_KEY,algorithms=ALGO)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid token")
