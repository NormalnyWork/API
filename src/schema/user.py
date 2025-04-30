from pydantic import BaseModel, EmailStr, field_validator

from utils import get_password_hash


class UserBase(BaseModel):
    email: EmailStr | None = None
    password: str | None = None

    @field_validator("password")
    @classmethod
    def password_validator(cls, value: str) -> str:
        return get_password_hash(value)

    class Config:
        from_attributes = True


class UserIn(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_validator(cls, value: str) -> str:
        return get_password_hash(value)

    class Config:
        from_attributes = True



class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class UserAuth(BaseModel):
    email: EmailStr
    password: str