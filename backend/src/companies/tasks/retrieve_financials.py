from core.celery import app

from companies.services.decorator import depends_company
from companies.repository import CompanyRepository, FinancialRepository, PriceRepository

from sources.services import get_financial_source

from datetime import date

from loguru import logger

from typing import TYPE_CHECKING

import asyncio, time

if TYPE_CHECKING:
    from companies.models import Company


@app.task
@depends_company
def retrieve_financials(company: 'Company') -> None:
    source = get_financial_source(company=company)
    financial_repository = FinancialRepository(sync=True)
    price_repository = PriceRepository(sync=True)

    current_year, current_quarter = date.today().year, (date.today().month - 1) // 3 + 1

    for year in range(current_year - 11, current_year + 1):
        for quarter in range(0, 5):
            request_quarter = quarter or None
            is_financial_data_exists = financial_repository.exists(company=company, year=year, quarter=request_quarter)

            if is_financial_data_exists:
                continue

            financial = asyncio.run(
                source.get_financials(symbol=company.symbol, year=year, quarter=request_quarter)
            )

            if financial is None:
                continue

            time.sleep(1)

            prices = asyncio.run(
                source.get_historical_prices(symbol=company.symbol, year=year, quarter=request_quarter)
            )

            if len(prices) > 0:
                financial.min_stock_price = min(prices, key=lambda x: x.close).close
                financial.max_stock_price = max(prices, key=lambda x: x.close).close

            for price in prices:
                is_price_data_exists = price_repository.exists(company=company, timestamp=price.timestamp)

                if is_price_data_exists:
                    continue

                price_repository.create(company_id=company.id, **price.model_dump())

            financial_repository.create(company_id=company.id, source=company.data_source, **financial.model_dump())

            logger.info(f'[{company.symbol}] Stored financial data for {year}/{request_quarter}')

            time.sleep(0.5)


@app.task
@depends_company
def retrieve_company(company: 'Company') -> None:
    if company.employees and company.summary and company.short_name:
        return

    source = get_financial_source(company=company)
    repository = CompanyRepository(sync=True)

    company_info = asyncio.run(source.get_info(symbol=company.symbol))

    if not company.employees:
        company.employees = company_info.employees
    if not company.summary:
        company.summary = company_info.summary
    if not company.short_name:
        company.short_name = company_info.short_name

    repository.save(company)

    logger.info(f'[{company.symbol}] Updated company information')


@app.task
def resync_companies() -> None:
    repository = CompanyRepository(sync=True)
    companies = repository.find_all()
    successful_updates = 0

    for company in companies:
        try:
            retrieve_company(company=company)
            retrieve_financials(company=company)
            successful_updates += 1
        except:
            logger.exception('Error when updating a company from the list')

    assert successful_updates > 0, 'No company has been updated successfully'


__all__ = (
    'retrieve_financials',
    'retrieve_company',
    'resync_companies',
)
