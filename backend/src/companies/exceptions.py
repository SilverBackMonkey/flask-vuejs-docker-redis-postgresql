from core.exceptions import APIError

from starlette.status import HTTP_404_NOT_FOUND


class CompanyNotFound(APIError):
    status_code = HTTP_404_NOT_FOUND
    detail = 'Company not found'


class ForecastNotFound(APIError):
    status_code = HTTP_404_NOT_FOUND
    detail = 'Forecast not found'
