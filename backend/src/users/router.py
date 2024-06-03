from fastapi import APIRouter

from core.auth import auth_backend

from .dependencies import fastapi_users
from .schemas import UserCreateSchema, UserReadSchema


router = APIRouter()
router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_register_router(UserReadSchema, UserCreateSchema))
