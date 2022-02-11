from datetime import datetime

from dateutil.parser import parse
import pendulum
from pendulum import DateTime

from .utils import DatePeriod


def get_date_edges(day: DatePeriod | DateTime| datetime | str | int) -> tuple[DateTime, DateTime]:
    r = None
    match day:
        case day if day in DatePeriod:
            r = _get_period(day)

        case datetime():
            day = DateTime(year=day.year, month=day.month, day=day.day)
            r = day._start_of_day(), day._end_of_day()

        case int() | str():
            r = _get_previous(day)

    if r is None:
        r = _get_day_edges(pendulum.instance(parse(day)))
    if r is None:
        raise ValueError("wrong get_date_edges input")
    else:
        return r


def _get_previous(day: str | int) -> tuple[DateTime, DateTime]:
    if isinstance(day, str):
        day = day.lower()

    match day:
        case "monday" | "понедельник" | "1" | 1:
            return _get_day_edges(pendulum.now().previous(1))
        case "tuesday" | "вторник" | "2" | 2:
            return _get_day_edges(pendulum.now().previous(2))
        case "wednesday" | "среда" | "3" | 3:
            return _get_day_edges(pendulum.now().previous(3))
        case "thursday" | "четверг" | "4" | 4:
            return _get_day_edges(pendulum.now().previous(4))
        case "friday" | "пятница" | "5" | 5:
            return _get_day_edges(pendulum.now().previous(5))
        case "saturday" | "суббота" | "6" | 6:
            return _get_day_edges(pendulum.now().previous(6))
        case "sunday" | "воскресенье" | "0" | 0:
            return _get_day_edges(pendulum.now().previous(0))


def _get_period(period: DatePeriod | str):
    today = pendulum.now()
    match period:
        case DatePeriod.TODAY | DatePeriod.TODAY.value:
            return _get_day_edges(today)

        case DatePeriod.WEEK | DatePeriod.WEEK.value:
            return today._start_of_week(), today._end_of_week()

        case DatePeriod.MONTH | DatePeriod.MONTH.value:
            return today._start_of_month(), today._end_of_month()

        case DatePeriod.YEAR | DatePeriod.YEAR.value:
            return today._start_of_year(), today._end_of_year()


def _get_day_edges(day: DateTime) -> tuple[DateTime, DateTime]:
    return day._start_of_day(), day._end_of_day()
