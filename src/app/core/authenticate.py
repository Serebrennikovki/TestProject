from fastapi import Depends, HTTPException, status
from services.auth.cookieauth import OAuth2PasswordBearerWithCookie

from core.jwt_handler import verify_access_token

# Схема OAuth2 для получения токена из cookie
oauth2_scheme_cookie = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/token")

def authenticate_cookie(token: str=Depends(oauth2_scheme_cookie)) -> str:
    if not token:
        raise HTTPException( 
        status_code=status.HTTP_403_FORBIDDEN, 
        detail="Sign in for access"
        )
    token = token.removeprefix('Bearer ')
    decoded_token = verify_access_token(token) 
    return decoded_token["user"]