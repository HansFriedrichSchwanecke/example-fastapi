from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta



from sqlalchemy.orm import Session
from starlette import status
from . import schemas, models
from .database import get_db
from .config import settings

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECURITY_KEY = settings.security_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=120)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECURITY_KEY, algorithm='HS256')

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECURITY_KEY, algorithms='HS256')
        print(SECURITY_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)
        print(type(ALGORITHM))
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oath2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f'Could not validate credentials',
                                         headers={'WWW-Authenticate': "Bearer"})

    token = verify_access_token(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
