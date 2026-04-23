from fastapi import HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timezone
import time


SECRET_KEY='MY_UNIQUE_KEY'
EXPIRED_TIME=3600

def create_access_token(user: str) -> str:
    payload={
        'user':user,
        'expires': time.time() + EXPIRED_TIME
    }
    token = jwt.encode(payload, SECRET_KEY,algorithm='HS256')
    return token

def verify_access_token(token: str) -> dict:
    try:
        data = jwt.decode(token,
                        SECRET_KEY,
                        algorithms=['HS256'],
                        )
        expire = data.get('expires')
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не передан корректный токен"
            )
        if datetime.now(timezone.utc) > datetime.fromtimestamp(expire, tz=timezone.utc): 
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="время жизни токена истекло"
            )
        return data
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Некорректный токен')