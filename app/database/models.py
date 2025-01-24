from datetime import date, datetime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.functions import now
from sqlalchemy.types import INTEGER, TIMESTAMP, VARCHAR, BOOLEAN, DATE
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(INTEGER(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(64), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(60), nullable=False)
    is_admin: Mapped[bool] = mapped_column(BOOLEAN(), default=False)
    is_master: Mapped[bool] = mapped_column(BOOLEAN(), default=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=now())

    sessions: Mapped[list["UserSession"]] = relationship(
        "UserSession", back_populates="user", cascade="all, delete-orphan"
    )


class UserSession(Base):
    __tablename__ = "user_session"
    id: Mapped[int] = mapped_column(INTEGER(), primary_key=True, autoincrement=True)
    expires: Mapped[date] = mapped_column(DATE(), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=now())

    user: Mapped[User] = relationship(User, back_populates="sessions")
