from __future__ import annotations

from sqlalchemy import BigInteger, Enum, ForeignKey, or_, and_
from sqlalchemy.orm import relationship, foreign, remote, Mapped, mapped_column

from core.db.base import BaseModel

from companies.types import FinancialSource
from companies.services import safe_math

from .company import Company

from typing import TYPE_CHECKING


class Financial(BaseModel):
    """ Financial data of the company """

    __tablename__ = 'financials'

    if TYPE_CHECKING:
        company_id: int
        company: Company
        source: FinancialSource
        year: int
        quarter: int
        net_income: int
        shares_outstanding: int
        free_cash_flow: float
        cash_flow_from_operating_activities: float
        dividends_per_share: float
        revenue: int
        capex: int
        total_assets: int
        total_liabilities: int
        net_debt: int
        interest_coverage: float
        dividend_yield: float
        min_stock_price: float
        max_stock_price: float
        price_earnings_ratio_ltm: float
        previous: 'Financial'
    else:
        company_id: Mapped[int] = mapped_column(ForeignKey(f'{Company.__tablename__}.id', ondelete='CASCADE'))
        company: Mapped[Company] = relationship(backref='financials')
        # Information about the company to which the data is linked

        source = mapped_column(Enum(FinancialSource))
        # What financial source did the data come from

        year: Mapped[int] = mapped_column()
        # The year for which the data is saved

        quarter: Mapped[int] = mapped_column(default=None, nullable=True)
        # The quarter for which the data is saved

        net_income: Mapped[int] = mapped_column(BigInteger, default=None, nullable=True)
        # Net income of company per period

        shares_outstanding: Mapped[int] = mapped_column(BigInteger, default=None, nullable=True)
        # Number of shares outstanding as the difference between issued shares and treasury shares

        free_cash_flow: Mapped[float] = mapped_column(default=None, nullable=True)
        # Free Cash Flow

        cash_flow_from_operating_activities: Mapped[float] = mapped_column(default=None, nullable=True)
        # Cash Flow from Operations

        dividends_per_share: Mapped[float] = mapped_column(default=None, nullable=True)
        # Dividend paid per share of the accounting period

        revenue: Mapped[int] = mapped_column(BigInteger, default=None, nullable=True)
        # Total revenue as reported on the income statement

        capex: Mapped[int] = mapped_column(BigInteger, default=None, nullable=True)
        # Capital expenditures, from cash flows from investing section of the cash flow statement

        total_assets: Mapped[int] = mapped_column(BigInteger, default=None, nullable=True)
        # Total company assets

        total_liabilities: Mapped[int] = mapped_column(BigInteger, default=None, nullable=True)
        # Total company liabilities

        net_debt: Mapped[int] = mapped_column(BigInteger, default=None, nullable=True)
        # Net Debt (including cash)

        interest_coverage: Mapped[float] = mapped_column(default=None, nullable=True)
        # EBIT divided by net interest expense

        dividend_yield: Mapped[float] = mapped_column(default=None, nullable=True)
        # Company dividend yield

        min_stock_price: Mapped[float] = mapped_column(default=None, nullable=True)
        # Minimum share price

        max_stock_price: Mapped[float] = mapped_column(default=None, nullable=True)
        # Maximum share price

        price_earnings_ratio_ltm: Mapped[float] = mapped_column(default=None, nullable=True)
        # Price to Earnings ratio

        minority_interest: Mapped[float] = mapped_column(default=0, server_default='0')
        # Represents the portion of earnings/losses of a subsidiary pertaining to
        # common stock not owned by the controlling company or other members of the consolidated group

        previous: Mapped['Financial'] = relationship(
            primaryjoin=or_(
                and_(remote(foreign(year)) == year - 1, quarter == None, remote(foreign(quarter)) == None),
                and_(remote(foreign(year)) == year, quarter != None, remote(foreign(quarter)) == quarter - 1),
                and_(remote(foreign(year)) == year - 1, quarter != None, remote(foreign(quarter)) == 4),
            ),
            uselist=False,
            order_by=(remote(foreign(year)).desc(), remote(foreign(quarter)).desc()),
        )
        # Prior financials data

    @property
    def earnings_per_share(self):
        return safe_math.divide(self.net_income, self.shares_outstanding)

    @property
    def free_cash_flow_per_share(self):
        return safe_math.divide(self.free_cash_flow, self.shares_outstanding)

    @property
    def dividends_payout(self):
        retention_ratio = safe_math.divide(
            safe_math.subtract(self.earnings_per_share, self.dividends_per_share),
            self.earnings_per_share,
        )
        return safe_math.subtract(1, retention_ratio)

    @property
    def revenue_change(self):
        try:
            return self._revenue_change
        except AttributeError:
            return self.previous and safe_math.subtract(safe_math.divide(self.revenue, self.previous.revenue), 1)

    @revenue_change.setter
    def revenue_change(self, value: float):
        self._revenue_change = value

    @property
    def margin(self):
        try:
            return self._margin
        except AttributeError:
            return safe_math.divide(self.net_income, self.revenue)

    @margin.setter
    def margin(self, value: float):
        self._margin = value

    @property
    def percentage_cfo_of_revenue(self):
        try:
            return self._percentage_cfo_of_revenue
        except AttributeError:
            return safe_math.divide(self.cash_flow_from_operating_activities, self.revenue)

    @percentage_cfo_of_revenue.setter
    def percentage_cfo_of_revenue(self, value: float):
        self._percentage_cfo_of_revenue = value

    @property
    def capex_change(self):
        try:
            return self._capex_change
        except AttributeError:
            return self.previous and safe_math.subtract(safe_math.divide(self.capex, self.previous.capex), 1)

    @capex_change.setter
    def capex_change(self, value: float):
        self._capex_change = value

    @property
    def free_cash_flow_yield(self):
        return safe_math.divide(self.free_cash_flow, self.average_market_cap)

    @property
    def total_assets_change(self):
        try:
            return self._total_assets_change
        except AttributeError:
            return self.previous and safe_math.subtract(
                safe_math.divide(self.total_assets, self.previous.total_assets), 1,
            )

    @total_assets_change.setter
    def total_assets_change(self, value: float):
        self._total_assets_change = value

    @property
    def percentage_liabilities_of_assets(self):
        try:
            return self._percentage_liabilities_of_assets
        except AttributeError:
            return self.previous and safe_math.divide(self.total_liabilities, self.previous.total_assets)

    @percentage_liabilities_of_assets.setter
    def percentage_liabilities_of_assets(self, value: float):
        self._percentage_liabilities_of_assets = value

    @property
    def shareholders_equity(self):
        return safe_math.subtract(self.total_assets, self.total_liabilities)

    @property
    def shares_outstanding_change(self):
        try:
            return self._shares_outstanding_change
        except AttributeError:
            return self.previous and safe_math.subtract(
                safe_math.divide(self.shares_outstanding, self.previous.shares_outstanding), 1,
            )

    @shares_outstanding_change.setter
    def shares_outstanding_change(self, value: float):
        self._shares_outstanding_change = value

    @property
    def roa(self):
        return safe_math.divide(self.net_income, self.total_assets)

    @property
    def roe(self):
        return safe_math.divide(self.net_income, self.shareholders_equity)

    @property
    def average_market_cap(self):
        return safe_math.multiply(self.average_stock_price, self.shares_outstanding)

    @property
    def average_stock_price(self):
        value = safe_math.fold(self.max_stock_price, self.min_stock_price)
        return value and value / 2

    @property
    def price_book_ratio(self):
        return safe_math.divide(self.market_price_per_share, self.book_value_per_share)

    @property
    def stock_price_range(self):
        if self.max_stock_price and self.min_stock_price:
            return f'{round(self.min_stock_price)}-{round(self.max_stock_price)}'
