from companies.types import ChartPeriod

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from typing import assert_never


def get_label_by_period(
    period: ChartPeriod,
    year: int = None,
    quarter: int = None,
    month: int = None,
    day: int = None,
) -> str:
    if period in (ChartPeriod.TEN_YEARS, ChartPeriod.FIVE_YEARS):
        return str(year)
    elif period == ChartPeriod.YEAR:
        return f'Q{quarter}/{year}'
    elif period in (ChartPeriod.MONTH, ChartPeriod.SIX_MONTHS):
        return f'{month}-{day}'
    return ''


def fill_gaps(
    source: list,
    period: ChartPeriod,
    fill_range: list[datetime, datetime],
    fill_period: timedelta | relativedelta,
) -> list:
    target = []
    previous_value = 0
    i = 0

    timestamps = tuple(x[1] for x in source)
    min_timestamp = min(*timestamps, fill_range[0])
    max_timestamp = max(*timestamps, fill_range[1])

    match period:
        case ChartPeriod.TEN_YEARS | ChartPeriod.FIVE_YEARS:
            check_keys = ['year']
        case ChartPeriod.YEAR:
            check_keys = ['year', 'quarter']
        case ChartPeriod.MONTH | ChartPeriod.SIX_MONTHS:
            check_keys = ['year', 'month', 'day']
        case _ as unreachable:
            assert_never(unreachable)
            return

    check_quarter = 'quarter' in check_keys
    if check_quarter:
        check_keys.remove('quarter')

    while (timestamp := min_timestamp + fill_period * i) <= max_timestamp:
        i += 1

        timestamp_quarter = (timestamp.month - 1) // 3 + 1
        index = None

        for x, source_timestamp in enumerate(timestamps):
            current_context = {x: getattr(timestamp, x) for x in check_keys}
            source_context = {x: getattr(source_timestamp, x) for x in check_keys}

            current_delta = relativedelta(**current_context)
            source_delta = relativedelta(**source_context)

            if current_delta == source_delta:
                if check_quarter is True:
                    source_quarter = (source_timestamp.month - 1) // 3 + 1
                    if source_quarter != timestamp_quarter:
                        continue

                index = x

                break

        if index is not None:
            value = previous_value = source[index][0]
        else:
            value = previous_value

        quarter = (timestamp.month - 1) // 3 + 1
        label = get_label_by_period(
            period=period,
            year=timestamp.year,
            quarter=quarter,
            month=timestamp.month,
            day=timestamp.day,
        )

        target.append([value, timestamp, label])

    return target


__all__ = (
    'get_label_by_period',
    'fill_gaps',
)
