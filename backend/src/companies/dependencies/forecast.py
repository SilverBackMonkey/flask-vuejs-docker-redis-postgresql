from fastapi import Depends

from users.dependencies import current_user

from companies.exceptions import ForecastNotFound
from companies.schemas import ForecastSchema

from .company import valid_company_symbol
from .repository import use_forecast_repository, use_forecast_field_repository

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from companies.models import Company, Forecast
    from companies.repository import ForecastRepository
    from users.models import User


async def valid_forecast_id(
    forecast_id: int,
    company: 'Company' = Depends(valid_company_symbol),
    repository: 'ForecastRepository' = Depends(use_forecast_repository),
    user: 'User' = Depends(current_user),
) -> 'Forecast':
    forecast = await repository.find_one(id=forecast_id, user=user, company=company)

    if not company:
        raise ForecastNotFound(symbol='forecast_id')

    return forecast


async def get_schema_by_forecast(forecast: 'Forecast') -> ForecastSchema:
    """
    Make a schema from forecast instance

    :param forecast: Forecast object
    :return: Forecast schema with values
    """

    repository = use_forecast_field_repository()

    values = {}

    fields = await repository.find_all(forecast=forecast)

    for stored_field in fields:
        if stored_field.column not in values:
            values[stored_field.column] = {}
        values[stored_field.column][stored_field.field] = stored_field.value

    return ForecastSchema(
        id=forecast.id,
        name=forecast.name,
        values=values,
        updated_at=forecast.updated_at,
    )


async def get_user_forecasts(
    company: 'Company' = Depends(valid_company_symbol),
    repository: 'ForecastRepository' = Depends(use_forecast_repository),
    user: 'User' = Depends(current_user),
) -> list[ForecastSchema]:
    forecasts = await repository.find_all(company=company, user=user)
    schemas = []

    for forecast in forecasts:
        schemas.append(await get_schema_by_forecast(forecast))

    return schemas


__all__ = (
    'valid_forecast_id',
    'get_schema_by_forecast',
    'get_user_forecasts',
)
