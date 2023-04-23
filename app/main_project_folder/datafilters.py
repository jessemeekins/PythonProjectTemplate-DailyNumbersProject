"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""
import re
from datetime import datetime
from typing import Dict, List, Set, Tuple, Union

class ReportType:
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
    def field_personnel(data: Dict[str, str]) -> bool:
        region = data["region"]
        is_field = re.search(r'D\d\dB\d\d', region)
        return is_field
    
    @staticmethod
    def bc_or_dc_working(data: Dict[str, str]) -> bool:
        unit = data["unit"]
        pattern = r'^[BD][C,D]\d{3}$'
        is_chief = re.search(pattern, unit)
        return is_chief

    @staticmethod
    def find_numbers_greater_than_two(data: Dict[str, str]) -> List[str]:
        string = data["detail_code"]
        pattern = r'\b([3-9]|[1-9][0-9]+)\b'
        numbers = re.findall(pattern, string)
        return numbers


class AlsCompanyReport(ReportType):
    def __init__(self, data: Dict[str, Dict[str, str]]) -> None:
        self.data = data

    def list_als_companies(self) -> Dict[str, Set[str]]:
        als_set = dict()
        for record in self.data.values():
            on_duty = self.on_duty(record)
            right_now = self.right_now(record)
            paramedic = self.is_paramedic(record)
            comp = self.get_company(record)

            if on_duty and paramedic and right_now:
                if any(x in comp for x in ['PU0', 'TR0', 'RC0', 'QT0']):
                    region = self.get_region(record)
                    if region not in als_set:
                        als_set[region] = set()
                    als_set[region].add(comp)
            else:
                pass
        return als_set

    @staticmethod
    def als_count(als_comp: Dict[str, Set[str]]) -> int:
        comp_lst = [i for v in als_comp.values() for i in v]
        return len(comp_lst)

    def __call__(self) -> Dict[str, Set[str]]:
        company_dict = self.list_als_companies()
        count = self.als_count(company_dict)
        print(f"[{datetime.now()}] ALS Count: {count}")
        return company_dict


class AssignmentReport(ReportType):
    def __init__(self, data: Dict[str, Dict[str, Union[str, List[str]]]]) -> None:
        self.data: Dict[str, Dict[str, Union[str, List[str]]]] = data

    def all_records(self) -> List[Tuple[str, str, str, str, str, str, List[str]]]:
        records = []
        for d in self.data.values():
            if d["pay_info"] == "FD Pay Info 1":
                shift = next((s[0] for s in d["specialities"] if "SH" in s), "No shift listed")
                comp = next((c for c in d["specialities"] if any(x in c for x in ['PU0', 'TR0', 'RC0', 'QT0', 'BC0'])), "No company listed")
                records.append((shift, comp, d["eid"], d["rank"], d["last_name"], d["first_name"], d["groups"]))
        return records

    def __call__(self) -> List[Tuple[str, str, str, str, str, str, List[str]]]:
        data = self.all_records()
        return data


class FullRosterReport(ReportType):
    def __init__(self, data: Dict[str, Dict[str, str]]) -> None:
        self.data = data

    def payroll_code_count(self) -> Dict[str, List[Dict[str, str]]]:
        grouped = {}
        for value in self.data.values():
            is_field = self.field_personnel(value)
            right_now = self.right_now(value)

            paycode = value["paycode"]
            if is_field and right_now:
                if paycode not in grouped.keys():
                    grouped[paycode] = []
                grouped[paycode].append({"rank": value["rank"], "name": value["name"]})

        return grouped

    def paycode_count(self) -> Dict[str, int]:
        count_dict = dict()
        grouped = self.payroll_code_count()
        for paycode, lst in grouped.items():
            count_dict[paycode] = len(lst)
        return count_dict

    def on_duty_chiefs(self) -> Dict[str, str]:
        chiefs = dict()
        for value in self.data.values():
            on_duty = self.on_duty(value)
            is_chief = self.bc_or_dc_working(value)
            if on_duty and is_chief:
                rank = value["rank"]
                name = value["name"]
                comp = value["unit"]
                if rank == "DC-FIRE":
                    chiefs[comp] = name
                elif rank == "BC-FIRE":
                    chiefs[comp] = name
                else:
                    pass
        return chiefs

    def off_by_rank(self) -> Dict[str, List[str]]:
        off_by_rank = dict()
        for value in self.data.values():
            is_field = self.field_personnel(value)
            off_duty = self.off_duty(value)

            if off_duty and is_field:
                rank = value["rank"]

                if rank[0] == '.':
                    rank = rank[1:]
                else:
                    rank
                if rank not in off_by_rank.keys():
                    off_by_rank[rank] = []
                off_by_rank[rank].append(value["name"])
        return off_by_rank

    def off_by_rank_count(self) -> Dict[str, int]:
        off_count = dict()
        ranks = self.off_by_rank()
        for rank, lst in ranks.items():
            off_count[rank] = len(lst)
        return off_count

    def multiple_days_off(self) -> Dict[str, Dict[str, Union[str, str]]]:
        sl = dict()
        for value in self.data.values():
            is_field = self.field_personnel(value)
            greater_than_two = self.find_numbers_greater_than_two(value)

            if value["paycode"] == "SL":

                if value["detail_code"] != 'Not listed' and is_field and greater_than_two:
                    sl[value["name"]] = {"paycode": value["paycode"], "days_off": greater_than_two[0]}
        return sl
    
    def get_current_shift(self) -> str:
        shifts = dict()
        for value in self.data.values():
            shift = self.get_shift(value)

            if shift not in shifts.keys():
                shifts[shift] = 0
            shifts[shift] += 1
        
        return max(shifts.items(), key=lambda x: x[1])[0][0]

    def __call__(self) -> Dict[str, Union[Dict[str, str], Dict[str, int], Dict[str, Dict[str, Union[str, str]]], Dict[str, Dict[str, Set[str]]]]]:
        als_report = AlsCompanyReport(self.data)
        als_comp = als_report.list_als_companies()
        als_count = als_report.als_count(als_comp)
        chiefs = self.on_duty_chiefs()
        paycodes = self.paycode_count()
        multi_day = self.multiple_days_off()
        off_by_rank = self.off_by_rank_count()
        shift = self.get_current_shift()
        return {'shift': shift,'chiefs': chiefs, "paycodes": paycodes, "multi_day": multi_day, "als": {"companies": als_comp, "count": als_count}, "off_by_rank": off_by_rank}

from typing import Dict, List
import re

class PayCodes(ReportType):
    PAYCODE_GROUPS = [
        ("Scheduled Day", r"SD|SDACT|WSB"),
        ("Vacation Leave", r"VL|VCALL|VL$"),
        ("Overtime", r"OT(CB|HO|R)?|EXT"),
        ("Bereavment", r"BV"),
        ("Suspended", r"SWOP|SWP"),
        ("Sick Leave", r"SL"),
        ("LWOP", r"LWOP"),
        ("OJI", r"OJI")
    ]

    def __init__(self, data: Dict[str, Dict[str, str]]) -> None:
        self.data = data

    def payroll_code_count(self) -> Dict[str, List[Dict[str, str]]]:
        grouped = {group[0]: [] for group in self.PAYCODE_GROUPS}
        
        for value in self.data.values():
            is_field = self.field_personnel(value)
            right_now = self.right_now(value)
            paycode = value["paycode"]

            if is_field and right_now:
                for group in self.PAYCODE_GROUPS:
                    pattern = group[1]
                    if re.search(pattern, paycode):
                        grouped[group[0]].append({"rank": value["rank"], "name": value["name"]})
                        break

        return grouped


    def paycode_count(self) -> Dict[str, int]:
        count_dict = dict()
        grouped = self.payroll_code_count()
        for paycode, lst in grouped.items():
            count_dict[paycode] = len(lst)
        return count_dict
    
    def total_people(self) -> str:
        num_working = list()
        for value in self.data.values():
            on_duty = self.on_duty(value)
            right_now = self.right_now(value)
            is_field = self.field_personnel(value)
            has_shift = self.twenty_four_hour_shift(value)

            if on_duty and right_now and is_field and has_shift:
                num_working.append(value["shift"])
        return len(num_working)
                


    def __call__(self):
        num = self.total_people()
        paycode = self.paycode_count()
        return {"paycode": paycode, "num_working": [num]}
    
  