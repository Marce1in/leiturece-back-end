from datetime import date, datetime
from typing import Optional
from sqlalchemy import func, text
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import TIMESTAMP, VARCHAR, BOOLEAN, DATE, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.database.db import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(VARCHAR(64), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(72), nullable=False)
    is_admin: Mapped[bool] = mapped_column(BOOLEAN(), default=False)
    is_master: Mapped[bool] = mapped_column(BOOLEAN(), default=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(), server_default=func.now())

    sessions: Mapped[Optional[list["UserSession"]]] = relationship(
        "UserSession", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', sessions={self.sessions})"


class UserSession(Base):
    __tablename__ = "user_session"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    expire_date: Mapped[date] = mapped_column(
        DATE(),
        nullable=False,
        server_default=text("CURRENT_DATE + INTERVAL '3 MONTH'"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(), server_default=func.now())

    user: Mapped[User] = relationship(User, back_populates="sessions")

    def __repr__(self) -> str:
        return f"UserSession(session_id={self.id}, user_id={self.user_id}, expire_date={self.expire_date})"
