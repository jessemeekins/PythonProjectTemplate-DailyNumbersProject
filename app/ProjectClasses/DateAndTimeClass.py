from dateutil import tz
from datetime import datetime, timedelta

class DateTimeFormatter:
    def utc_timestamp() -> datetime:
        return datetime.now(tz=tz.tzutc())
        
    def local_timestamp() -> datetime:
        return datetime.now(tz=tz.tzlocal())

    def shift_start_end_adjust() -> str:
        today = datetime.today() - timedelta(hours=7)
        formatted_time = datetime.strftime(today, "%Y-%m-%d")
        print(formatted_time)
        return formatted_time
    
    def currently_working(start_and_end_time: tuple) -> bool:
        sdate, stime = start_and_end_time[0].split('T')
        edate, etime = start_and_end_time[1].split('T')
        stime, _ = start_and_end_time[0].split("-")
        etime, _ = start_and_end_time[1].split("-")
        start_time = datetime.strptime(sdate+" "+stime, "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.strptime(edate+" "+etime, "%Y-%m-%d %H:%M:%S.%f")
        now = datetime.now()

        return now > start_time and now < end_time