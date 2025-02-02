from typing import Annotated
from fastapi import APIRouter, Body, HTTPException, status

from datetime import date, timedelta

from sqlalchemy import select, or_

from app.dependencies.mail.body import body

from ..dependencies.database.db import db_dependency
from ..dependencies.database.models import EmailCheck, User

from ..dependencies.mail.mail import email_dependency

from ..schemas.auth import UserLogin, UserRegister
from ..helpers.auth import hash_secret

from ..settings import config

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/")
async def auth():
    pass


@router.post("/login")
async def login():
    pass


@router.post("/mail/{mail_hash}")
async def mail_verify(mail_hash: str, db: db_dependency):
    email = await db.scalar(
        select(EmailCheck).where(EmailCheck.email_hash == mail_hash)
    )

    if email is None:
        return HTTPException(status.HTTP_401_UNAUTHORIZED, "Hash inválido")

    user = await db.scalar(select(User).where(User.id == email.user_id))

    if user is None:
        return HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")

    user.email_verified = True
    await db.delete(email)
    await db.commit()

    return {"message": "E-mail verificado com sucesso"}


@router.post("/register")
async def register(
    new_user: Annotated[UserRegister, Body()],
    db: db_dependency,
    mail: email_dependency,
):

    user = await db.scalar(
        select(User).where(
            or_(User.email == new_user.email, User.name == new_user.name)
        )
    )

    if user is not None:
        if user.email == new_user.email:
            return HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Esse E-mail já está sendo usado"
            )
        elif user.name == new_user.name:
            return HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Esse Nome já está sendo usado"
            )
        # This should be impossible to reach
        else:
            return HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Algo deu errado... (⊙_⊙')"
            )

    hash_passwd = hash_secret(new_user.password)
    hash_email = hash_secret(new_user.email)

    db.add(
        User(
            name=new_user.name,
            email=new_user.email,
            password=hash_passwd,
            email_check=EmailCheck(
                email_hash=hash_email, expires=date.today() + timedelta(days=1)
            ),
        )
    )
    await db.commit()

    html_body, text_body = body.email_verification(hash_email)
    await mail.send_email(
        "Código de verificação Leiturece", new_user.email, html_body, text_body
    )

    return {"message": "FOI, olha o email boi"}


@router.post("/logout")
async def logout():
    pass
