from dateutil import tz
from datetime import datetime, timedelta

class DateTimeFormatter:
    def __init__(self) -> None:
        pass
        
    def utc_timestamp() -> datetime:
        return datetime.now(tz=tz.tzutc())
        
    def local_timestamp() -> datetime:
        return datetime.now(tz=tz.tzlocal())

    def shift_start_end_adjust() -> str:
        today = datetime.today() - timedelta(hours=7)
        formatted_time = datetime.strftime(today, "%Y-%m-%d")
        print(formatted_time)
        return formatted_time 