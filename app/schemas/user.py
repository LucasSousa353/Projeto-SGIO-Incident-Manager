from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "operador"

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool
