from typing import Annotated
from fastapi import APIRouter, Body
from pydantic import BaseModel, EmailStr, Field
from app.database.db import db_dependency

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

class UserRegister(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=4, max_length=1024)

class UserLogin(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=4, max_length=1024)


@router.get("/")
def auth():
    pass

@router.post("/login")
def login():
    pass

@router.post("/register")
def register(new_user: Annotated[UserRegister, Body()]):
    return new_user


@router.post("/logout")
def logout():
    pass
