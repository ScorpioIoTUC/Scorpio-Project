from datetime import datetime

def datetime_to_string(dt: datetime, format_string: str = "%Y-%m-%dT%H:%M:%S") -> str:
    return dt.strftime(format_string)

def now():
    return datetime.now()

def diff_seconds(start: datetime, end: datetime) -> float:
    return (end - start).total_seconds()
    