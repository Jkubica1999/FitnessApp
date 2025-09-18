from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.models import User
from app.schemas.user import UserCreate
from app.utils import hash_password, verify_password

# Retrieve a user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Retrieve a user by ID
def get_user_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()

# Create a new user, ensuring email uniqueness and password hashing
def create_user(db: Session, user_in: UserCreate) -> User:
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
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Authenticate a user by verifying email and password, pylance type checking gives an error, but everything works fine, so ignore it
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash): # type: ignore
        return None
    return user
