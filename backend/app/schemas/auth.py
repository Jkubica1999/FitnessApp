from pydantic import BaseModel, EmailStr, Field

# Schema for user login credentials
class Login(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

# Schema for authentication token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
