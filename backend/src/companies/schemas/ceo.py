from core.schemas.base import BaseSchema


class CEOSchema(BaseSchema):
    full_name: str
    start_year: int
    end_year: int | None = None


__all__ = (
    'CEOSchema',
)
