#%%
import re
import json
from datetime import datetime
from typing import Tuple, Dict


json_file = "/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/json/full_roster_export2023-05-11.json"


def ISO_8601_reformatter(start_and_end_time: tuple) -> tuple[datetime,datetime]:
    sdate, stime = start_and_end_time[0].split('T')
    edate, etime = start_and_end_time[1].split('T')
    stime, _ = stime.split("-")
    etime, _ = etime.split("-")
    start_time = datetime.strptime(sdate+" "+stime, "%Y-%m-%d %H:%M:%S.%f")
    end_time = datetime.strptime(edate+" "+etime, "%Y-%m-%d %H:%M:%S.%f")
    return (start_time, end_time)

def get_tupled_times(data: dict[str, str]) -> Tuple[str, str]:
    return (data["StaffingStartDt"], data["StaffingEndDt"])

def currently_working(tupled_times: Tuple[datetime, datetime]) -> bool:
    now = datetime.now()
    return now > tupled_times[0] and now < tupled_times[1]


def working_record(record: dict) -> bool:
    return record['WstatIsWorkingGm'] == 'true'


def working_shift(record: dict()) -> bool:
    shift = record['ShiftAbrvCh']
    specialities = record['RscFormulaIDCh']
    return shift in specialities

def region_in_field(record: Dict[str, str]) -> bool:
    region = record["RegionAbrvCh"]
    is_field = re.search(r'D\d\dB\d\d', region)
    return is_field


with open(json_file) as file:
    data = file.read()
    file_data = json.loads(data)

records = file_data['DataRoot']['Data']['Records']['Record']
count = 0
otcb = 0
for record in records:
    try:
        tupled_times = get_tupled_times(record)
        formatted_times = ISO_8601_reformatter(tupled_times)
        is_working = currently_working(formatted_times)   
        is_onduty = working_record(record)
        is_current_shift = working_shift(record)
        is_field = region_in_field(record)
        
        if is_working and is_current_shift and is_onduty and record["WstatAbrvCh"] == "SD":
            count += 1
        if is_working and is_onduty and is_field and record["WstatAbrvCh"] == 'OTCB':
            otcb += 1
    except:
        ...     
            
            
                
        
        
print("[*] Regular Duty: ",count)
print("[*] OTCB: ",otcb)