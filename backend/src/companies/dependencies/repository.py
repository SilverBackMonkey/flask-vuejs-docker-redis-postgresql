from companies.repository import *


def use_company_repository() -> CompanyRepository:
    return CompanyRepository()


def use_financial_repository() -> FinancialRepository:
    return FinancialRepository()


def use_ceo_repository() -> CEORepository:
    return CEORepository()


def use_forecast_repository() -> ForecastRepository:
    return ForecastRepository()


def use_forecast_field_repository() -> ForecastFieldRepository:
    return ForecastFieldRepository()


__all__ = (
    'use_company_repository',
    'use_financial_repository',
    'use_ceo_repository',
    'use_forecast_repository',
    'use_forecast_field_repository',
)

