from companies.repository import CompanyRepository

from typing import Callable, TYPE_CHECKING
from functools import wraps

if TYPE_CHECKING:
    from companies.models import Company


def depends_company(function: Callable) -> Callable:
    @wraps(function)
    def _function(company: 'Company' = None, symbol: str = None, **kwargs) -> None:
        repository = CompanyRepository(sync=True)

        if not company:
            if not symbol:
                raise TypeError('retrieve_company() missing 1 required positional argument: \'symbol\'')

            company = repository.find_one(symbol=symbol)

            if not company:
                raise ValueError(f'retrieve_company() unknown symbol: \'{symbol}\'')

        function(company=company, **kwargs)

    return _function


__all__ = (
    'depends_company',
)
