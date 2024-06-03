from fastapi import Depends

from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase

from core.db import get_async_db_session
from core.auth import auth_backend

from .models import User
from .managers import UserManager
from .repository import UserRepository

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


def use_user_repository() -> UserRepository:
    return UserRepository()


async def get_user_database(session: 'AsyncSession' = Depends(get_async_db_session)) -> SQLAlchemyUserDatabase:
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_database)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)


__all__ = (
    'get_user_database',
    'get_user_manager',
    'fastapi_users',
    'current_user',
)
