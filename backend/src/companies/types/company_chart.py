from typing import TypeAlias

from companies.schemas.chart_schema import ChartSchema


CompanyChart: TypeAlias = dict[str, list[ChartSchema]]


__all__ = (
    'CompanyChart',
)
