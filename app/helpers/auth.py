import bcrypt
from uuid import uuid4
from datetime import timedelta
from typing import Annotated
from fastapi import Cookie, HTTPException, Response
from joserfc.errors import ExpiredTokenError
from sqlalchemy import select
from ..settings import config
from ..dependencies.database.db import db_dependency
from ..dependencies.database.models import UserSession
from ..dependencies.token.token import token_dependency


def verify_secret(secret: str, hash_secret: str) -> bool:
    return bcrypt.checkpw(
        bytes(secret, encoding="utf-8"),
        bytes(hash_secret, encoding="utf-8"),
    )


def hash_secret(secret: str) -> str:
    return str(
        bcrypt.hashpw(
            bytes(secret, encoding="utf-8"),
            bcrypt.gensalt(),
        )
    )


def generate_uuid() -> str:
    return uuid4().hex


def set_access_token_cookie(token: str, response: Response, expire_minutes: int):
    response.set_cookie(
        key="ACCESS_TOKEN",
        value=token,
        httponly=True,
        secure=config.SECURE_COOKIES,
        domain=config.BACKEND_DOMAIN,
        samesite="lax",
        path="/",
        max_age=int(timedelta(minutes=expire_minutes).total_seconds()),
    )


def set_refresh_token_cookie(token: str, response: Response, expire_days: int):
    response.set_cookie(
        key="REFRESH_TOKEN",
        value=token,
        httponly=True,
        secure=config.SECURE_COOKIES,
        domain=config.BACKEND_DOMAIN,
        samesite="lax",
        path="/",
        max_age=int(timedelta(days=expire_days).total_seconds()),
    )


async def verify_auth(
    response: Response,
    jwt: token_dependency,
    db: db_dependency,
    REFRESH_TOKEN: Annotated[str | None, Cookie()] = None,
    ACCESS_TOKEN: Annotated[str | None, Cookie()] = None,
):
    if not REFRESH_TOKEN:
        raise HTTPException(401, "Usuário deslogado")

    try:
        if not ACCESS_TOKEN:
            raise ExpiredTokenError
        else:
            jwt.decode_jwt(ACCESS_TOKEN)

    except ExpiredTokenError:
        try:
            refresh_token = jwt.decode_jwt(REFRESH_TOKEN)
        except:
            raise HTTPException(401, "Token inválido")

        session = await db.scalar(
            select(UserSession).where(UserSession.id == refresh_token.claims["sub"])
        )
        if not session:
            raise HTTPException(401, "Token inválido")

        token = jwt.generate_jwt({"sub": str(session.user_id)}, expire_minutes=30)
        set_access_token_cookie(token, response, expire_minutes=30)

    except:
        raise HTTPException(401, "Token inválido")
