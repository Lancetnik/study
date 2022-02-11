from enum import Enum, EnumMeta


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True    


class BaseEnum(Enum, metaclass=MetaEnum):
    pass


class DatePeriod(BaseEnum):
    TODAY = 'today'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'