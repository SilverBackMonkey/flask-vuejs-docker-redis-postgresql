from enum import Enum


class FinancialPeriod(Enum):
    ANNUAL = 'annual'
    QUARTERLY = 'quarterly'


__all__ = (
    'FinancialPeriod',
)
