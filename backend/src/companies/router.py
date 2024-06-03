from fastapi import APIRouter, Depends, Body

from fastapi_cache.decorator import cache

from users.dependencies import current_user

from .services.forecast import create_forecast, save_forecast
from .types import CompanyChart, ForecastValue
from .schemas import CompanySchema, FinancialResponseSchema, ValuationEarningsSchema, ForecastCreateSchema, \
    ForecastSchema, CompanySimpleSchema
from .dependencies import get_company_with_market_data, get_company_financials, get_company_ceo, \
    get_valuation_and_earnings, get_company_chart, valid_company_symbol, valid_forecast_id, get_user_forecasts, \
    get_schema_by_forecast, get_companies_list

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Company, Financial, CEO, Forecast
    from users.models import User


router = APIRouter()


@router.get('/', response_model=list[CompanySimpleSchema])
async def retrieve_companies(
    companies: list[CompanySimpleSchema] = Depends(get_companies_list),
) -> list[CompanySimpleSchema]:
    return companies


@router.get('/{symbol}', response_model=CompanySchema)
@cache(expire=10)
async def retrieve_company(
    company: CompanySchema = Depends(get_company_with_market_data),
    _: 'User' = Depends(current_user),
) -> CompanySchema:
    return company


@router.get('/{symbol}/financials', response_model=FinancialResponseSchema)
@cache(expire=600)
async def retrieve_financials(
    financials: list['Financial'] = Depends(get_company_financials),
    ceo: list['CEO'] = Depends(get_company_ceo),
    _: 'User' = Depends(current_user),
) -> FinancialResponseSchema | dict:
    return {
        **financials,
        'ceo': ceo,
    }


@router.get('/{symbol}/valuation_and_earnings', response_model=ValuationEarningsSchema)
@cache(expire=300)
async def retrieve_valuation_and_earnings(
    valuation_and_earnings: ValuationEarningsSchema = Depends(get_valuation_and_earnings),
    _: 'User' = Depends(current_user),
) -> ValuationEarningsSchema:
    return valuation_and_earnings


@router.get('/{symbol}/chart/{period}', response_model=CompanyChart)
# @cache(expire=600)
async def retrieve_chart_data(
    chart_data: CompanyChart = Depends(get_company_chart),
    _: 'User' = Depends(current_user),
) -> CompanyChart:
    return chart_data


@router.get('/{symbol}/forecast', response_model=list[ForecastSchema])
async def retrieve_forecasts(
    forecasts: list['ForecastSchema'] = Depends(get_user_forecasts),
) -> list['ForecastSchema']:
    return forecasts


@router.post('/{symbol}/forecast/create', response_model=ForecastSchema)
async def create_forecast_router(
    forecast: ForecastCreateSchema,
    company: 'Company' = Depends(valid_company_symbol),
    user: 'User' = Depends(current_user),
) -> dict:
    forecast = await create_forecast(forecast.name, company, user)

    return {
        'id': forecast.id,
        'name': forecast.name,
        'values': {},
    }


@router.post('/{symbol}/forecast/{forecast_id}/save', response_model=ForecastSchema)
async def save_forecast_router(
    payload: ForecastValue = Body(),
    forecast: 'Forecast' = Depends(valid_forecast_id),
) -> ForecastSchema:
    forecast = await save_forecast(forecast, payload)
    return await get_schema_by_forecast(forecast)
