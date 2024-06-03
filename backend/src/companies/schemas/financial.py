from core.schemas.base import BaseSchema

from companies.types import Percentage


class FinancialMetaSchema(BaseSchema):
    year: int | str | None = None
    quarter: int | None = None
    net_income: int | None = None
    shares_outstanding: int | None = None
    free_cash_flow: float | None = None
    cash_flow_from_operating_activities: float | None = None
    dividends_per_share: float | None = None
    dividend_yield: Percentage | None = None
    revenue: int | None = None
    capex: int | None = None
    total_assets: int | None = None
    total_liabilities: int | None = None
    net_debt: int | None = None
    interest_coverage: float | None = None
    min_stock_price: float | None = None
    max_stock_price: float | None = None
    price_earnings_ratio_ltm: float | None = None
    minority_interest: float = 0


class FinancialSchema(FinancialMetaSchema):
    free_cash_flow_yield: Percentage | None = None
    free_cash_flow_per_share: float | None = None
    percentage_cfo_of_revenue: Percentage | None = None
    dividends_payout: Percentage | None = None
    revenue_change: Percentage | None = None
    margin: Percentage | None = None
    capex_change: Percentage | None = None
    shareholders_equity: float | None = None
    roa: Percentage | None = None
    roe: Percentage | None = None
    earnings_per_share: float | None = None
    total_assets_change: Percentage | None = None
    percentage_liabilities_of_assets: float | None = None
    shares_outstanding_change: Percentage | None = None
    average_market_cap: float | None = None
    average_stock_price: float | None = None
    stock_price_range: str | None = None


__all__ = (
    'FinancialMetaSchema',
    'FinancialSchema',
)
