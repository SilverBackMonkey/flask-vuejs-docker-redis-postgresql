from core.schemas.base import BaseSchema

from .financial import FinancialSchema
from .ceo import CEOSchema


class FinancialResponseSchema(BaseSchema):
    financials: list[FinancialSchema]
    # average: list[FinancialSchema]
    # terminal: list[FinancialSchema]
    ceo: list[CEOSchema]


__all__ = (
    'FinancialResponseSchema',
)
