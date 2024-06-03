from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_users.db import SQLAlchemyBaseUserTable

from core.db.base import BaseModel

from typing import TYPE_CHECKING


class User(SQLAlchemyBaseUserTable[int], BaseModel):
    """ User in the TopFunds system """

    __tablename__ = 'users'

    if TYPE_CHECKING:
        email: str
        hashed_password: str
        is_active: bool
        is_superuser: bool
        is_verified: bool
    else:
        email: Mapped[str] = mapped_column(
            String(length=320), unique=True, index=True, nullable=False
        )
        hashed_password: Mapped[str] = mapped_column(
            String(length=1024), nullable=False
        )
        is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
        is_superuser: Mapped[bool] = mapped_column(
            Boolean, default=False, nullable=False
        )
        is_verified: Mapped[bool] = mapped_column(
            Boolean, default=False, nullable=False
        )


__all__ = (
    'User',
)
