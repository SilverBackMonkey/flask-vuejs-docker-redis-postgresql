from core.schemas import BaseSchema

from companies.types import Percentage


class ValuationEarningsSchema(BaseSchema):
    free_cash_flow_yield: Percentage | None = None
    dividend_yield: Percentage | None = None
    market_cap: float | None = None

    price_earnings_ratio_ltm: float | None = None
    price_book_ratio: float | None = None
    peg: float | None = None

    total_return_ltm: Percentage | None = None
    total_return_5y: Percentage | None = None
    total_return_10y: Percentage | None = None

    free_cash_flow_per_share_ltm: Percentage | None = None
    free_cash_flow_per_share_5y: Percentage | None = None
    free_cash_flow_per_share_10y: Percentage | None = None

    earnings_per_share_ltm: Percentage | None = None
    earnings_per_share_5y: Percentage | None = None
    earnings_per_share_10y: Percentage | None = None


__all__ = (
    'ValuationEarningsSchema',
)
