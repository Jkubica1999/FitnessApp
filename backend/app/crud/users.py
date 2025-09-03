from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.models import User
from app.schemas.user import UserCreate
from app.utils import hash_password, verify_password


def get_user_by_email(db: Session, email: str):
    """Return a User by email, or None if not found."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Create a new user.
    - Reject duplicate emails (400).
    - Hash the password before storing.
    """
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    db_user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        role=user_in.role or "athlete",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    """
    Check credentials.
    - Return User if valid.
    - Return None if invalid (caller will raise 401).
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
