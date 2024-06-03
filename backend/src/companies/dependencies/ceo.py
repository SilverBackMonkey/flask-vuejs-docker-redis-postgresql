from sqlalchemy import text

from fastapi import Depends

from .company import valid_company_symbol
from .repository import use_ceo_repository

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from companies.repository import CEORepository
    from companies.models import Company, CEO


async def get_company_ceo(
    company: 'Company' = Depends(valid_company_symbol),
    repository: 'CEORepository' = Depends(use_ceo_repository),
) -> list['CEO']:
    """
    Gets a list of the CEO of the company

    :param company: Company model object
    :param repository:
    :return: List of CEO model objects
    """

    return await repository.find_all(company=company, order=text('start_year ASC'))


__all__ = (
    'get_company_ceo',
)
