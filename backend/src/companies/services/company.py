from sqlalchemy import select, func, extract, asc, desc, text, and_

from core.db import get_async_session_maker

from sources.services import get_financial_source

from companies.models import Price, Financial
from companies.types import ChartPeriod
from companies.schemas import ChartSchema
from companies.repository import FinancialRepository

from .helpers import get_label_by_period, fill_gaps

from dateutil.relativedelta import relativedelta

from typing import TYPE_CHECKING
from datetime import datetime, timedelta, timezone

if TYPE_CHECKING:
    from companies.models import Company


async def get_company_financial_data(company: 'Company', period: ChartPeriod, field: str) -> list[ChartSchema]:
    repository = FinancialRepository()
    current_timestamp = datetime.now(timezone.utc)
    current_quarter = (current_timestamp.month - 1) // 3 + 1

    reverse = False
    query_args = [Financial.company == company]
    query_kwargs = {}

    if period in (ChartPeriod.TEN_YEARS, ChartPeriod.FIVE_YEARS):
        query_kwargs['order'] = text('year ASC')
        query_args += [
            Financial.year >= current_timestamp.year - (11 if period == ChartPeriod.TEN_YEARS else 6),
            Financial.year != current_timestamp.year,
            Financial.quarter == None,
        ]
    elif period == (ChartPeriod.YEAR):
        reverse = True
        query_kwargs['limit'] = 4
        query_kwargs['order'] = text('year DESC, quarter DESC')
        query_args += [
            Financial.quarter != None,
            ~and_(
                Financial.year == current_timestamp.year,
                Financial.quarter == current_quarter,
            ),
        ]
    else:
        return []

    financials = await repository.find_all(*query_args, **query_kwargs)
    if reverse:
        financials = financials[::-1]

    schemas = []

    for financial in financials:
        schemas.append(ChartSchema(
            label=get_label_by_period(period=period, year=financial.year, quarter=financial.quarter),
            value=getattr(financial, field, None) or 0,
        ))

    return schemas


async def get_company_stock_prices(company: 'Company', period: ChartPeriod) -> list[ChartSchema]:
    select_stmt = [func.avg(Price.close), func.max(Price.timestamp)]
    group_by_stmt = [Price.company_id]
    order_by_stmt = []
    query_stmt = [Price.company == company]
    limit = None
    reverse = False

    current_timestamp = datetime.now(timezone.utc).replace(tzinfo=None)
    current_quarter = (current_timestamp.month - 1) // 3 + 1

    fill_limit = None

    source = get_financial_source(company)

    if period in (ChartPeriod.TEN_YEARS, ChartPeriod.FIVE_YEARS):
        select_stmt += [extract('year', Price.timestamp).label('label')]
        group_by_stmt += ['label']
        order_by_stmt += [asc('label')]

        year = extract('year', Price.timestamp)
        query_stmt.append(year != current_timestamp.year)

        if period == ChartPeriod.TEN_YEARS:
            query_stmt.append(year >= current_timestamp.year - 11)
        else:
            query_stmt.append(year >= current_timestamp.year - 6)

        fill_range = [current_timestamp, current_timestamp]
        fill_period = relativedelta(years=1)
    elif period == ChartPeriod.YEAR:
        quarter = func.floor((extract('month', Price.timestamp) - 1) / 3 + 1)
        year = extract('year', Price.timestamp)

        select_stmt += [
            func.concat('Q', quarter, '/', year).label('label'),
            quarter, year,
        ]

        group_by_stmt += [year, quarter]
        order_by_stmt += [desc(year), desc(quarter)]
        query_stmt += [~and_(year == current_timestamp.year, quarter == current_quarter)]

        limit = 4

        reverse = True

        fill_range = [current_timestamp, current_timestamp]
        fill_period = relativedelta(months=3)
    elif period in (ChartPeriod.MONTH, ChartPeriod.SIX_MONTHS):
        day = extract('day', Price.timestamp)
        month = extract('month', Price.timestamp)

        select_stmt += [
            func.concat(month, '-', day).label('label'),
            day, month,
        ]

        group_by_stmt += [day, month]
        order_by_stmt += [asc(month), asc(day)]

        from_timestamp = current_timestamp.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)

        if period == ChartPeriod.MONTH:
            from_timestamp -= timedelta(days=40)
        else:
            from_timestamp -= timedelta(days=240)

        query_stmt.append(Price.timestamp >= from_timestamp)

        fill_range = [current_timestamp, current_timestamp]
        fill_period = relativedelta(days=1)
        fill_limit = 30 if period == ChartPeriod.MONTH else 180
    elif period in (ChartPeriod.FIVE_DAYS, ChartPeriod.DAY):
        prices = await source.get_last_prices(symbol=company.symbol)

        if period == ChartPeriod.DAY:
            last_timestamp = prices[-1].timestamp
            index = 0

            for i, point in enumerate(prices[::-1]):
                if point.timestamp.day < last_timestamp.day:
                    index = i
                    break

            prices = prices[-index:]

        schemas = []

        for point in prices:
            schemas.append(ChartSchema(
                label=point.timestamp.strftime('%m-%d %H:%M'),
                value=point.close,
            ))

        return schemas

    statement = select(*select_stmt).filter(*query_stmt).group_by(*group_by_stmt).order_by(*order_by_stmt)
    if limit is not None:
        statement = statement.limit(limit)

    async with get_async_session_maker() as session:
        result = await session.execute(statement)

    result = result.all()
    if reverse is True:
        result = result[::-1]

    result = fill_gaps(
        source=result,
        period=period,
        fill_range=fill_range,
        fill_period=fill_period,
    )[-(fill_limit or 0):]

    stock_price, _, _, _ = await source.get_stock_price(symbol=company.symbol)
    result[-1][0] = stock_price

    schemas = []

    for point in result:
        schemas.append(ChartSchema(
            label=str(point[2]),
            value=point[0],
        ))

    return schemas


__all__ = (
    'get_company_stock_prices',
)
