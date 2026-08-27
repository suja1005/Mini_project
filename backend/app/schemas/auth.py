from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    full_name: str
    email: str
    password: str
    degree: Optional[str] = "B.Tech"
    department: Optional[str] = "Computer Science"

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    degree: Optional[str] = "B.Tech"
    department: Optional[str] = "Computer Science"
