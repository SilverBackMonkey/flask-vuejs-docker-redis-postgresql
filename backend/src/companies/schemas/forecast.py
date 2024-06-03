from core.schemas import BaseSchema

from companies.types.forecast import ForecastValue

from datetime import datetime


class ForecastCreateSchema(BaseSchema):
    name: str


class ForecastSchema(BaseSchema):
    id: int
    name: str
    values: ForecastValue
    updated_at: datetime


__all__ = (
    'ForecastCreateSchema',
    'ForecastSchema',
)
