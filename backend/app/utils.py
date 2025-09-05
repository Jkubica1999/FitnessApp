#Password hashing and verification utilities

from passlib.context import CryptContext


_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:

    return _pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:

    return _pwd_context.verify(plain_password, hashed_password)

#JWT token creation and decoding utilities

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: Dict[str, Any], expires_minutes: Optional[int] = None) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {**data, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Dict[str, Any]:
    # Raises JWTError on invalid/expired token
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
