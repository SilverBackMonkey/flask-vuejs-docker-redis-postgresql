from core.schemas.base import BaseSchema

from decimal import Decimal


class ChartSchema(BaseSchema):
    label: str
    value: int | float | Decimal

__all__ = (
    'ChartSchema',
)
