from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.users import get_user_by_id
from app.utils import decode_access_token

# OAuth2 scheme for extracting bearer token from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Dependency to get the current authenticated user from the token
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
    except Exception:
        raise cred_exc

    sub = payload.get("sub")
    if not sub:
        raise cred_exc

    user = get_user_by_id(db, sub)
    if not user:
        raise cred_exc
    return user
