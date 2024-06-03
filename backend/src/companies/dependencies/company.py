from sqlalchemy import text, and_

from fastapi import Depends

from companies.exceptions import CompanyNotFound
from companies.schemas import CompanySchema, ValuationEarningsSchema
from companies.models import Company, Financial
from companies.types import ChartPeriod, CompanyChart
from companies.services.company import get_company_stock_prices, get_company_financial_data
from .repository import use_company_repository, use_financial_repository

from sources.services import get_financial_source

import companies.services.safe_math as safe_math

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from companies.repository import CompanyRepository, FinancialRepository


async def valid_company_symbol(
    symbol: str,
    repository: 'CompanyRepository' = Depends(use_company_repository),
) -> Company:
    """
    Looking for a company based on the transferred symbol

    :param symbol: Used to search for a related company
    :param repository: Company Repository
    :return: Company model object
    """

    company = await repository.find_one(symbol=symbol)

    if not company:
        raise CompanyNotFound(field='symbol')

    return company


async def get_company_with_market_data(
    company: Company = Depends(valid_company_symbol),
) -> CompanySchema:
    schema = CompanySchema.model_validate(company)
    source = get_financial_source(company)

    schema.stock_price, schema.stock_price_change, \
        schema.week_52_high, schema.week_52_low = await source.get_stock_price(symbol=company.symbol)

    return schema


async def get_companies_list(repository: 'CompanyRepository' = Depends(use_company_repository)) -> list[Company]:
    """
    Retrieve companies list

    :param repository: Company Repository
    :return: List of the company objects
    """

    return await repository.find_all()


async def get_valuation_and_earnings(
    company: Company = Depends(valid_company_symbol),
    repository: 'FinancialRepository' = Depends(use_financial_repository),
) -> ValuationEarningsSchema:
    """
    Find and aggregate company statistics

    :param company: Company model object
    :param repository:
    :return: Valuation and Earnings schema
    """

    source = get_financial_source(company)

    valuation_and_earnings = await source.get_stats(symbol=company.symbol)

    financial = await repository.find_one(company=company, order=text('year DESC, quarter DESC'))
    previous_financials = await repository.find_all(
        Financial.company == company,
        Financial.quarter == None,
        Financial.year.in_([
            financial.year - 1, financial.year - 5, financial.year - 10,
        ]),
        order=text('year DESC'),
    )

    for i, period in enumerate(('ltm', '5y', '10y')):
        if len(previous_financials) <= i:
            break

        previous = previous_financials[i]

        setattr(
            valuation_and_earnings,
            f'free_cash_flow_per_share_{period}',
            safe_math.subtract(
                safe_math.divide(financial.free_cash_flow_per_share, previous.free_cash_flow_per_share),
                1,
            )
        )

        setattr(
            valuation_and_earnings,
            f'earnings_per_share_{period}',
            safe_math.subtract(
                safe_math.divide(financial.earnings_per_share, previous.earnings_per_share),
                1,
            )
        )

    return valuation_and_earnings


async def get_company_chart(
    period: ChartPeriod,
    company: Company = Depends(valid_company_symbol),
) -> CompanyChart:
    stock_price = await get_company_stock_prices(company, period)
    free_cash_flow_per_share = await get_company_financial_data(company, period, 'free_cash_flow_per_share')
    earnings_per_share = await get_company_financial_data(company, period, 'earnings_per_share')
    
    chart_data = {}

    if stock_price:
        chart_data['stock_price'] = stock_price
    if free_cash_flow_per_share:
        chart_data['free_cash_flow_per_share'] = free_cash_flow_per_share
    if earnings_per_share:
        chart_data['earnings_per_share'] = earnings_per_share

    return chart_data


__all__ = (
    'valid_company_symbol',
    'get_companies_list',
    'get_company_with_market_data',
    'get_valuation_and_earnings',
    'get_company_chart',
)
