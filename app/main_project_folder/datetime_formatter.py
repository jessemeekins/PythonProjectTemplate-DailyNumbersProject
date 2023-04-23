"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""

from dateutil import tz
from datetime import datetime, timedelta

class DateTimeFormatter:
    @staticmethod        
    def utc_timestamp() -> datetime:
        return datetime.now(tz=tz.tzutc())

    @staticmethod    
    def local_timestamp() -> datetime:
        return datetime.now(tz=tz.tzlocal())

    @staticmethod
    def shift_start_end_adjust() -> str:
        today = datetime.today() - timedelta(hours=7)
        formatted_time = datetime.strftime(today, "%Y-%m-%d")
        return formatted_time 