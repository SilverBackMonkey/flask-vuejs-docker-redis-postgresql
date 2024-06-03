from companies.models import Financial
from companies.schemas import FinancialSchema

from datetime import datetime, timezone
from typing import get_args


def calculate_financials_average(financials: list[Financial]) -> FinancialSchema:
    schema = FinancialSchema(year='Average (A)')

    timestamp = datetime.now(timezone.utc)
    target_financials = [x for x in financials if x.year < timestamp.year if isinstance(x.year, int)]

    for name, field in FinancialSchema.model_fields.items():
        try:
            field_type = get_args(field.annotation)[0]
            average_value = field_type(sum(getattr(x, name) or 0 for x in target_financials) / len(target_financials))
            setattr(schema, name, average_value)
        finally:
            continue

    return schema


# async def calculate_forecast(
#     financial: Financial,
#     forecast: list[ForecastData],
# ) -> tuple[list[FinancialSchema], FinancialSchema]:
#     data = []
#
#     for forecast_by_period in forecast:
#         projected_financial = Financial()
#         projected_financial.previous = financial
#
#         projected_financial.year = forecast_by_period.year
#         projected_financial.revenue_change = forecast_by_period.revenue_change
#         projected_financial.margin = forecast_by_period.margin
#         projected_financial.percentage_cfo_of_revenue = forecast_by_period.percentage_cfo_of_revenue
#         projected_financial.capex_change = forecast_by_period.capex_change
#         projected_financial.total_assets_change = forecast_by_period.total_assets_change
#         projected_financial.percentage_liabilities_of_assets = forecast_by_period.percentage_liabilities_of_assets
#         projected_financial.shares_outstanding_change = forecast_by_period.shares_outstanding_change
#
#         projected_financial.revenue = safe_math.multiply(
#             financial.revenue,
#             safe_math.fold(1, projected_financial.revenue_change / 100),
#         )
#
#         if projected_financial.revenue:
#             projected_financial.revenue = int(projected_financial.revenue)
#
#         projected_financial.net_income = safe_math.multiply(projected_financial.revenue, projected_financial.margin)
#
#         if projected_financial.net_income:
#             projected_financial.net_income = int(projected_financial.net_income)
#
#         projected_financial.cash_flow_from_operating_activities = safe_math.multiply(
#             projected_financial.revenue,
#             projected_financial.percentage_cfo_of_revenue,
#         )
#
#         projected_financial.capex = safe_math.multiply(
#             financial.capex,
#             safe_math.fold(1, projected_financial.capex_change),
#         )
#
#         if projected_financial.capex:
#             projected_financial.capex = int(projected_financial.capex)
#
#         projected_financial.total_assets = safe_math.multiply(
#             financial.total_assets,
#             safe_math.fold(1, financial.total_assets_change),
#         )
#
#         if projected_financial.total_assets:
#             projected_financial.total_assets = int(projected_financial.total_assets)
#
#         projected_financial.total_liabilities = safe_math.multiply(
#             projected_financial.total_assets,
#             projected_financial.percentage_liabilities_of_assets,
#         )
#
#         if projected_financial.total_liabilities:
#             projected_financial.total_liabilities = int(projected_financial.total_liabilities)
#
#         projected_financial.shares_outstanding = safe_math.multiply(
#             financial.shares_outstanding,
#             safe_math.fold(1, projected_financial.shares_outstanding_change),
#         )
#
#         if projected_financial.shares_outstanding:
#             projected_financial.shares_outstanding = int(projected_financial.shares_outstanding)
#
#         projected_financial.free_cash_flow = safe_math.fold(
#             projected_financial.cash_flow_from_operating_activities, projected_financial.capex,
#         )
#
#         financial = projected_financial
#         data.append(financial)
#
#     return data[:-1], data[-1]


__all__ = (
    'calculate_financials_average',
)
