from fastapi import APIRouter, Body, Depends, HTTPException, Response, Cookie
from typing import Annotated

from sqlalchemy import select, or_

from ..dependencies.mail.body import body

from ..dependencies.database.db import db_dependency
from ..dependencies.database.models import User, UserSession

from ..dependencies.mail.mail import email_dependency
from ..dependencies.token.token import token_dependency

from ..schemas.auth import UserRegister, UserLogin
from ..helpers.auth import (
    set_refresh_token_cookie,
    set_refresh_token_cookie,
    verify_secret,
    verify_auth,
    hash_secret,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/", dependencies=[Depends(verify_auth)])
async def auth():
    return {"message": "Usuário está logado"}


@router.post("/login")
async def login(
    db: db_dependency,
    jwt: token_dependency,
    user_data: UserLogin,
    response: Response,
    REFRESH_TOKEN: Annotated[str | None, Cookie()] = None,
):
    if REFRESH_TOKEN:
        return {"message": "Usuário já está logado"}

    email = user_data.email
    password = user_data.password

    user = await db.scalar(select(User).where(User.email == email))

    if not user:
        raise HTTPException(401, "E-mail ou senha inválidos")
    elif not verify_secret(password, user.password):
        raise HTTPException(401, "E-mail ou senha inválidos")

    user_session = UserSession(user_id=user.id)

    db.add(user_session)
    await db.commit()
    await db.refresh(user_session)

    token = jwt.generate_jwt(
        payload={"sub": str(user_session.id)}, expire_minutes=90 * 60 * 24
    )
    set_refresh_token_cookie(token, response, expire_days=90)

    return {"message": "Login foi um sucesso"}


@router.post("/register")
async def register(
    new_user: Annotated[UserRegister, Body()],
    db: db_dependency,
    mail: email_dependency,
    jwt: token_dependency,
):

    user = await db.scalar(
        select(User).where(
            or_(User.email == new_user.email, User.name == new_user.name)
        )
    )

    if user:
        if user.email == new_user.email:
            raise HTTPException(401, "Esse E-mail já está sendo usado")
        elif user.name == new_user.name:
            raise HTTPException(401, "Esse Nome já está sendo usado")
        # This should be impossible to reach
        else:
            raise HTTPException(401, "Algo deu errado... (⊙_⊙')")

    hash_passwd = hash_secret(new_user.password)

    payload = {
        "name": new_user.name,
        "email": new_user.email,
        "password": hash_passwd,
    }

    token = jwt.generate_jwt(payload, expire_minutes=15, is_encrypted=True)

    html_body, text_body = body.email_verification(token)
    await mail.send_email(
        "Código de verificação Leiturece", new_user.email, html_body, text_body
    )

    return {"message": "Registro feito com sucesso"}


@router.post("/register/{encoded_token}")
async def verify_register(encoded_token: str, db: db_dependency, jwt: token_dependency):
    try:
        token = jwt.decode_jwt(encoded_token, True)
        payload = UserRegister(**token.claims)
    except:
        raise HTTPException(400, "Token inválido")

    user = await db.scalar(
        select(User).where(or_(User.email == payload.email, User.name == payload.name))
    )
    if user:
        raise HTTPException(400, "E-mail já verificado ou essa conta já existe")

    db.add(User(name=payload.name, password=payload.password, email=payload.email))
    await db.commit()

    return {"message": "E-mail Verificado com sucesso"}


@router.post("/logout")
async def logout(
    response: Response,
    db: db_dependency,
    jwt: token_dependency,
    REFRESH_TOKEN: Annotated[str | None, Cookie()] = None,
):
    if REFRESH_TOKEN:
        try:
            payload = jwt.decode_jwt(REFRESH_TOKEN)
            session_id = payload.claims.get("sub")
            session = await db.scalar(
                select(UserSession).where(UserSession.id == session_id)
            )
            if session:
                await db.delete(session)
                await db.commit()
        except:
            pass

    response.delete_cookie("REFRESH_TOKEN")
    response.delete_cookie("ACCESS_TOKEN")

    return {"message": "Usuário deslogado com sucesso"}


@router.post("/passchange")
async def passchange():
    pass


@router.post("/passchange/{token}")
async def verify_change():
    pass
