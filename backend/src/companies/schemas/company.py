from core.schemas.base import BaseSchema

from companies.types import Percentage


class CompanySimpleSchema(BaseSchema):
    symbol: str
    name: str


class CompanyMetaSchema(BaseSchema):
    short_name: str | None = None
    founded: int | None = None
    employees: int | None = None
    summary: str | None = None


class CompanySchema(CompanyMetaSchema):
    symbol: str
    name: str
    keywords: str
    logo: str | None = None
    stock_price: float | None = None
    stock_price_change: Percentage | None = None
    week_52_high: float | None = None
    week_52_low: float | None = None


__all__ = (
    'CompanySimpleSchema',
    'CompanySchema',
    'CompanyMetaSchema',
)
