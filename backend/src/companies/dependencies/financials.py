from sqlalchemy import text
from sqlalchemy.orm import selectinload

from fastapi import Depends

from companies.types import FinancialPeriod
from companies.models import Financial

from .company import valid_company_symbol
from .repository import use_financial_repository

from typing import assert_never, TYPE_CHECKING

if TYPE_CHECKING:
    from companies.repository import FinancialRepository
    from companies.models import Company


async def get_company_financials(
    period: FinancialPeriod = FinancialPeriod.ANNUAL,
    company: 'Company' = Depends(valid_company_symbol),
    repository: 'FinancialRepository' = Depends(use_financial_repository),
) -> dict[str, list[Financial]]:
    """
    Retrieves all financial data for the company

    :param period: Quarter or year
    :param forecast:
    :param forecast_id:
    :param company: The company for which you need to find financial data
    :param repository: Financial Repository
    :return: List of financial data of the company
    """

    query_filters = [Financial.company == company]

    match period:
        case FinancialPeriod.ANNUAL:
            query_filters.append(Financial.quarter == None)
        case FinancialPeriod.QUARTERLY:
            query_filters.append(Financial.quarter != None)
        case _ as unreachable:
            assert_never(unreachable)

    financials = await repository.find_all(
        *query_filters,
        options=selectinload(Financial.previous),
        order=text('year ASC, quarter ASC'),
    )

    return {
        'financials': financials,
    }


__all__ = (
    'get_company_financials',
)
