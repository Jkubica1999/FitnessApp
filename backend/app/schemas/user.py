# User data validation and serialization schemas
from pydantic import BaseModel, EmailStr, Field, field_validator
import re

# Base schema for User, shared by create and output schemas
class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr

# Schema for creating a new User, includes password validation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        # Require at least one uppercase letter
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        # Require at least one lowercase letter
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        # Require at least one digit
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        # Require at least one special character
        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("Password must contain at least one special character")
        return v

# Output schema for returning User data to clients
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

