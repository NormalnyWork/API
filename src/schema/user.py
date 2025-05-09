from pydantic import BaseModel, EmailStr, field_validator, Field

from utils import get_password_hash


class UserBase(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    fcm_token: str | None = None
    timezone: str | None = None
    workday_start: int | None = None
    workday_end: int | None = None

    @field_validator("password")
    @classmethod
    def password_validator(cls, value: str) -> str:
        return get_password_hash(value)

    class Config:
        from_attributes = True


class UserIn(BaseModel):
    name: str
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
    name: str
    email: EmailStr
    timezone: str | None = None
    workday_start: int
    workday_end: int

    class Config:
        from_attributes = True


class UserAuth(BaseModel):
    email: EmailStr
    password: str