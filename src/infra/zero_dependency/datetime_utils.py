from src.libs.zero_dependency.datetime_utils import (
    datetime_to_string,
    now,
    diff_seconds,
)


class DateTimeUtils:
    @classmethod
    def datetime_to_string(cls, dt, format_string: str = "%Y-%m-%d %H:%M:%S"):
        return datetime_to_string(dt, format_string)

    @classmethod
    def now(cls):
        return now()

    @classmethod
    def diff_seconds(cls, start, end):
        return diff_seconds(start, end)
