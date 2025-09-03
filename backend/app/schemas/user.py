from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re

Role = Literal["athlete", "coach", "parent", "admin"]

class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    role: Optional[Role] = "athlete"

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        """
        Enforce strong password rules:
        - At least 8 chars (Field enforces this already).
        - At least one uppercase, one lowercase, one digit, one special char.
        """
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("Password must contain at least one special character")
        return v

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role

    class Config:
        from_attributes = True

