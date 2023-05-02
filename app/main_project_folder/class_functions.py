"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""
import re
from datetime import datetime
from typing import Dict, List, Set, Tuple, Union

class ReportType:
    def __init__(self, data: dict):
        self.data = data

        
    @staticmethod
    def ISO_8601_reformatter(start_and_end_time: tuple) -> tuple[datetime,datetime]:
        sdate, stime = start_and_end_time[0].split('T')
        edate, etime = start_and_end_time[1].split('T')
        stime, _ = stime.split("-")
        etime, _ = etime.split("-")
        start_time = datetime.strptime(sdate+" "+stime, "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.strptime(edate+" "+etime, "%Y-%m-%d %H:%M:%S.%f")
        return (start_time, end_time)

    @staticmethod
    def get_tupled_times(data: Dict[str, str]) -> Tuple[str, str]:
        return data["shift_start"], data["shift_end"]

    @staticmethod
    def currently_working(tupled_times: Tuple[datetime, datetime]) -> bool:
        now = datetime.now()
        return now > tupled_times[0] and now < tupled_times[1]

    @staticmethod
    def is_paramedic(data: Dict[str, Union[str, List[str]]]) -> bool:
        return data["rank"] == "FFP" or "EMTP" in data["specialties"]

    @staticmethod
    def is_battalion_chief(data: Dict[str, str]) -> bool:
        return data["rank"] == "BC"

    @staticmethod
    def is_division_chief(data: Dict[str, str]) -> bool:
        return data["rank"] == "DC"

    @staticmethod
    def get_company(data: Dict[str, str]) -> str:
        return data["unit"]
    @staticmethod
    def get_name(data: Dict[str, str]) -> str:
        return data["name"]
    @staticmethod
    def get_rank(data: Dict[str, str]) -> str:
        rank = data["rank"]
        return rank
        
    @staticmethod
    def get_paycode(data: Dict[str, str]) -> str:
        return data["paycode"]

    @staticmethod
    def get_shift(data: Dict[str, str]) -> str:
        return data["shift"]

    @staticmethod
    def get_region(data: Dict[str, str]) -> str:
        return data["region"]
    
    @staticmethod
    def on_duty(data: Dict[str, str]) -> bool:
        if data["is_working"] == 'true':
            t_times = ReportType.get_tupled_times(data)
            formatted_times = ReportType.ISO_8601_reformatter(t_times)
            on_duty = ReportType.currently_working(formatted_times)
            return on_duty
        else:
            return False
    
    @staticmethod
    def off_duty(data: Dict[str, str]) -> bool:
        return data['is_working'] == 'false'

    @staticmethod
    def right_now(data: Dict[str, str]) -> bool:
        t_times = ReportType.get_tupled_times(data)
        formatted_times = ReportType.ISO_8601_reformatter(t_times)
        on_duty = ReportType.currently_working(formatted_times)
        return on_duty

    @staticmethod
    def twenty_four_hour_shift(data: dict[str, str]) -> bool:
        shift = data["shift"]
        shifts = ["ASH", "BSH", "CSH"]
        if shift in shifts:
            return True
        else:
            False


    @staticmethod
    def region_in_field(data: Dict[str, str]) -> bool:
        region = data["region"]
        is_field = re.search(r'D\d\dB\d\d', region)
        return is_field
    
    @staticmethod
    def bc_or_dc_working(data: Dict[str, str]) -> bool:
        unit = data["unit"]
        rank = data["rank"]
        pattern = r'^[ABD][C,D]\d{3}$'
        is_chief_unit = re.search(pattern, unit)
        if '.' not in rank and is_chief_unit:
            return True

    @staticmethod
    def find_numbers_greater_than_two(data: Dict[str, str]) -> List[str]:
        string = data["detail_code"]
        pattern = r'\b([3-9]|[1-9][0-9]+)\b'
        numbers = re.findall(pattern, string)
        return numbers
    
    @staticmethod
    def get_current_shift(data: dict) -> str:
        shifts = dict()
        for value in data.values():
            shift = ReportType.get_shift(value)

            if shift not in shifts.keys():
                shifts[shift] = 0
            shifts[shift] += 1
        return max(shifts.items(), key=lambda x: x[1])[0]
    
    @staticmethod
    def is_field_compliment(data: Dict[str,str]) -> bool:
        if "FIELD" in data["specialties"]:
            return True

    @staticmethod
    def get_shift_specialty(shift, data: Dict[str, str]) -> bool:
        pattern = r"ASH|BSH|CSH" 
        
        specialties_shift = data["specialties"]
        specialties_shift = re.findall(pattern, specialties_shift)
        if specialties_shift:
            return shift == specialties_shift[0]
        else:
            ...
    @staticmethod
    def _get_shift_specialty(data: Dict[str, str]) -> str:
        pattern = r"ASH|BSH|CSH" 
        
        specialties_shift = data["specialties"]
        specialties_shift = re.findall(pattern, specialties_shift)
        if specialties_shift:
        
            return specialties_shift[0]
        else:
            "None"
            
    
    @staticmethod
    def get_specialty_company(data:dict) -> str:
        specialties = data["specialties"]
        pattern = r'\b[A-Z]{2}\d{3}\b'

        match = re.findall(pattern, specialties)

        if match:
            return  str(match[0])
        else:
            return 'None'
   


        
        
