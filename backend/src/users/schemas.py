from fastapi_users import schemas


class UserReadSchema(schemas.BaseUser[int]):
    pass


class UserCreateSchema(schemas.BaseUserCreate):
    pass


__all__ = (
    'UserReadSchema',
    'UserCreateSchema',
)
