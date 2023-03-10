from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True
