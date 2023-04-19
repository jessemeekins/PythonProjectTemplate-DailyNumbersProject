"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""
import re
import itertools
from datetime import datetime


class ReportTypeClass:
    def __init__(self) -> None:
        pass

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
    def _get_tupled_times(_data: dict) -> tuple:
        return (_data["shift_start"], _data["shift_end"])

    @staticmethod
    def _currently_working(tupled_times: tuple[datetime,datetime]) -> bool:
        now = datetime.now()
        try:
            return now > tupled_times[0] and now < tupled_times[1]
        except:
            return False

    @staticmethod
    def _paramedic(data:dict) -> bool:
        return data["rank"] == "FFP" or "EMTP" in data["specialties"]       
    
    @staticmethod
    def _battalion_chief(data: dict) -> bool:
        return data["rank"] == "BC"
    
    @staticmethod
    def _division_chief(data:dict) -> bool:
        return data["rank"] == "DC"
    
    @staticmethod
    def get_company(data:dict) -> str:
        return data["unit"]
    
    @staticmethod
    def _company_abrev_first_two_letters(data:str):
        return data["unit"][0:2]
    
    @staticmethod
    def _paycode(data:dict) -> str:
        return data["paycode"]
    
    @staticmethod
    def _shift(data:dict) -> str:
        return data["shift"]
    
    @staticmethod
    def is_working(data:dict) -> str:
        return data["is_working"]
    
    @staticmethod
    def get_region(data:dict) -> str:
        return data["region"]
    
    @staticmethod
    def get_station(data:dict) -> str:
        return data["station"]
    
    def _on_duty(self, data:dict) -> bool:
        if data["is_working"] == 'true':
            t_times = self._get_tupled_times(data)
            formatted_times = self.ISO_8601_reformatter(t_times)
            on_duty = self._currently_working(formatted_times)
            return on_duty
        else:
            return False
        
    def _off_duty(self, data:dict) -> bool:
        if data['is_working'] == 'false':
            return True
    
    def _field_personnel(self, data: dict) -> bool:
        region = data["region"]
        is_field = re.search(r'D\d\dB\d\d', region)
        return is_field
    
    def _bc_or_dc_working(self, data:dict) -> bool:
        unit = data["unit"]
        pattern = r'^[BD][C,D]\d{3}$'
        is_chief = re.search(pattern, unit)
        return is_chief
    
    
    def find_numbers_greater_than_two(self, data: dict) -> str:
        string = data["detail_code"]
        # Define a regular expression pattern to match numbers greater than 2
        pattern = r'\b([3-9]|[1-9][0-9]+)\b'
        # Use the findall() method to extract all matching numbers from the string
        numbers = re.findall(pattern, string)
        # Return the list of matching numbers
        return numbers


class AlsCompanyReport(ReportTypeClass):
    def __init__(self, data: dict) -> None:
        self.data = data
    
    def _list_als_companies(self) -> dict:
        """Mini Procotcal method for finding ALS companies in service"""
        als_set = dict()
        for i, record in enumerate(self.data.values()):
            on_duty = self._on_duty(record)
            paramedic = self._paramedic(record)

            comp = self.get_company(record)

            if on_duty and paramedic:
                if 'PU0' in comp or 'TR0' in comp or 'RC0' in comp or 'QT0' in comp:
                    region = self.get_region(record)
                    if region not in als_set:
                        als_set[region] = set()
                    als_set[region].add((comp)) 
            else:
                ...
        return als_set
    
    def als_count(self, als_comp: dict) -> int:
        comp_lst = list()
        for k, v in als_comp.items():
            for i in v:
                comp_lst.append(i)
        return len(comp_lst)
    
    def __call__(self) -> dict:
        company_dict = self._list_als_companies()
        count = self.als_count(company_dict)
        print(f"[{datetime.now()}] ALS Count: {count}")
        return company_dict
    



class AssignmentReport(ReportTypeClass):
    def __init__(self, data) -> None:
        self.data: dict = data

    def _all_records(self) -> list:
        records = list()
        for d in self.data.values():
            if d["pay_info"] == "FD Pay Info 1":
                shift = [s[0] for s in d["specialities"] if "SH" in s]
                if shift:
                    shift = shift[0]
                else:
                    shift = "No shift listed"
                comp = [c for c in d["specialities"] if "PU0" in c or "TR0" in c or "RC0" in c or "QT0" in c or "BC0" in c]
                if comp:
                    comp = comp[0]
                else:
                    comp = "No company listed"
            
                records.append((shift, comp, d["eid"], d["rank"], d["last_name"], d["first_name"], d["groups"]))
        return records
    
    def __call__(self) -> dict:
        data = self._all_records()
        return data
    

class FullRosterReport(ReportTypeClass):
    def __init__(self, data: dict) -> None:
        self.data = data

    def _payroll_code_count(self) -> dict:
        grouped = {}
        for value in self.data.values():
            is_field = self._field_personnel(value)
      
            paycode = value["paycode"]
            if is_field:
                if paycode not in grouped.keys():
                    grouped[paycode] = []
                grouped[paycode].append({"rank":value["rank"], "name": value["name"]}) 

        return grouped
    
    def _paycode_count(self):
        count_dict = dict()
        grouped = self._payroll_code_count()
        for paycode, lst in grouped.items():
            count_dict[paycode] = len(lst)
        return count_dict
        
    
    def _on_duty_chiefs(self) -> set:
        chiefs= dict()
        for value in self.data.values():
            on_duty = self._on_duty(value)
            is_chief = self._bc_or_dc_working(value)
            if on_duty and is_chief:
                rank = value["rank"]
                name = value["name"]
                comp = value["unit"]
                match rank:
                    case "DC-FIRE":
                        chiefs[comp] = name
                    case "BC-FIRE":
                        chiefs[comp] = name 
                    case other:
                        ...
        return chiefs
    
    def _off_by_rank(self) -> dict:
        off_by_rank = dict()
        for value in self.data.values():
            is_field = self._field_personnel(value)
            on_duty = self._off_duty(value)
            

            if on_duty and is_field:
                rank = value["rank"]

                if rank[0] == '.':
                    rank = rank[1:]
                else:
                    rank
                if rank not in off_by_rank.keys():
                    off_by_rank[rank] = []
                off_by_rank[rank].append(value["name"])
        return off_by_rank
    
    def _off_by_rank_count(self) -> dict:
        off_count = dict()
        ranks = self._off_by_rank()
        for rank, lst in ranks.items():
            off_count[rank] = len(lst)
        return off_count


    def multiple_days_off(self) -> dict:
        sl = dict()
        for value in self.data.values():
            is_field = self._field_personnel(value)
            greater_than_two = self.find_numbers_greater_than_two(value)

            if value["paycode"] == "SL":

                if value["detail_code"] != 'Not listed' and is_field and greater_than_two:
                    sl[value["name"]] = {"paycode": value["paycode"],"days_off": greater_than_two[0]}
        return sl
    

    def __call__(self) -> dict[dict]:
        class_als = AlsCompanyReport(self.data)
        als_comp = class_als._list_als_companies()
        als_count = class_als.als_count(als_comp)
        chiefs = self._on_duty_chiefs()
        paycodes = self._paycode_count()
        multi_day = self.multiple_days_off()
        off_by_rank = self._off_by_rank_count()

        return {'chiefs': chiefs, "paycodes": paycodes, "multi_day": multi_day, "als": {"companies": als_comp, "count": als_count}, "off_by_rank": off_by_rank}