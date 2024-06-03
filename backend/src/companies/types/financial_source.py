from enum import Enum


class FinancialSource(Enum):
    IEXCLOUD = 'iexcloud'
    POLYGONIO = 'polygonio'
    CUSTOM = 'custom'


__all__ = (
    'FinancialSource',
)
