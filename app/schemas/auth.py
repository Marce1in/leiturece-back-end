from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=4, max_length=1024)


class UserLogin(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=4, max_length=1024)
