from companies.models import Company, Forecast, ForecastField
from companies.dependencies.repository import use_forecast_repository, use_forecast_field_repository
from companies.types import ForecastValue
from companies.schemas import ForecastSchema

from users.models import User


async def create_forecast(name: str, company: Company, user: User) -> Forecast:
    """
    Create new user forecast

    :param name: Name of the forecast
    :param company: The company for which the forecast is being created
    :param user: The user who creates the forecast
    :return: Forecast object
    """

    repository = use_forecast_repository()
    return await repository.create(name=name, company_id=company.id, user_id=user.id)


async def save_forecast(forecast: Forecast, payload: ForecastValue) -> Forecast:
    """
    Creates or updates forecast data

    :param forecast: Forecast model instance
    :param payload: A dictionary in which the key is the forecast field and the value is a number
    :return: Forecast object
    """

    repository = use_forecast_field_repository()

    for column, fields in payload.items():
        for field, value in fields.items():
            stored_field = await repository.find_one(forecast=forecast, column=column, field=field)

            if not stored_field:
                stored_field = ForecastField(forecast_id=forecast.id, column=column, field=field, value=value)
            else:
                stored_field.value = value

            await repository.save(stored_field)

    return forecast
