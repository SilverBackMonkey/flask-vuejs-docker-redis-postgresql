from enum import Enum


class ChartPeriod(str, Enum):
    TEN_YEARS = '10Y'
    FIVE_YEARS = '5Y'
    YEAR = '1Y'
    SIX_MONTHS = '6M'
    MONTH = '1M'
    FIVE_DAYS = '5D'
    DAY = '1D'


__all__ = (
    'ChartPeriod',
)
