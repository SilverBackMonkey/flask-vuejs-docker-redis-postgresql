from core.schemas.base import BaseSchema

from datetime import datetime


class PriceSchema(BaseSchema):
    open: float
    high: float
    low: float
    close: float
    volume: float
    timestamp: datetime


__all__ = (
    'PriceSchema',
)
