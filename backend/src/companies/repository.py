from core.db.repository import SQLAlchemyRepository

from .models import Company, Financial, CEO, Price, Forecast, ForecastField


class CompanyRepository(SQLAlchemyRepository[Company]):
    model = Company


class FinancialRepository(SQLAlchemyRepository[Financial]):
    model = Financial


class CEORepository(SQLAlchemyRepository[CEO]):
    model = CEO


class PriceRepository(SQLAlchemyRepository[Price]):
    model = Price


class ForecastRepository(SQLAlchemyRepository[Forecast]):
    model = Forecast


class ForecastFieldRepository(SQLAlchemyRepository[ForecastField]):
    model = ForecastField


__all__ = (
    'CompanyRepository',
    'FinancialRepository',
    'CEORepository',
    'PriceRepository',
    'ForecastRepository',
    'ForecastFieldRepository',
)
