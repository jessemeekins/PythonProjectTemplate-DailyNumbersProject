"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""
import re
import itertools
from datetime import datetime
from openpyxl import Workbook

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
        return now > tupled_times[0] and now < tupled_times[1]

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
    def _company_identifier(data:dict) -> str:
        return data["company"]
    
    @staticmethod
    def _company_abrev_first_two_letters(data:str):
        return data["company"][0:2]
    
    @staticmethod
    def _paycode(data:dict) -> str:
        return data["paycode"]
    
    @staticmethod
    def _shift(data:dict) -> str:
        return data["shift"]
    
    def _on_duty(self, data:dict) -> bool:
        if data["is_working"] == 'true':
            t_times = self._get_tupled_times(data)
            formatted_times = self.ISO_8601_reformatter(t_times)
            on_duty = self._currently_working(formatted_times)
            return on_duty
        else:
            return False
    
    def _field_personnel(aelf, data: dict) -> bool:
        region = data["region"]
        is_field = re.search(r'D\d\dB\d\d', region)
        return is_field


class AlsCompanyReport(ReportTypeClass):
    def __init__(self, data: dict) -> None:
        self.data = data
    
    def _list_als_companies(self) -> dict:
        """Mini Procotcal method for finding ALS companies in service"""
        als_list = dict()
        for i, record in enumerate(self.data.values()):
            on_duty = self._on_duty(record)
            paramedic = self._paramedic(record)
            comp = self._company_identifier(record)

            if on_duty and paramedic:
                if 'PU0' in comp or 'TR0' in comp or 'RC0' in comp or 'QT0' in comp:
                    als_list[comp] = {"ALS": True}
            else:
                ...
        return als_list
    
    def als_count(self, als_comp: dict) -> int:
        return len(als_comp)
    
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
            on_duty = self._on_duty(value)
            is_field = self._field_personnel(value)
      
            paycode = value["paycode"]
            if on_duty and is_field:
                if paycode not in grouped.keys():
                    grouped[paycode] = []
                grouped[paycode].append({"rank":value["rank"], "name": value["name"]}) 
           
            
        #for paycode, lst in grouped.items():
            #print(f"[*] {paycode}: {len(lst)}")

        return grouped
    
    def _paycode_count(self):
        count_list = list()
        grouped = self._payroll_code_count()
        for paycode, lst in grouped.items():
            count_list.append(f"[*] {paycode}: {len(lst)}")
        return count_list
        
    
    def _on_duty_chiefs(self):
        dc = []
        bc = []

        for value in self.data.values():
            on_duty = self._on_duty(value)
            if on_duty:
                rank = value["rank"]
                name = value["name"]
                comp = value["unit"]
                match rank:
                    case "DC-FIRE":
                        dc.append((comp+': ' +name))
                    case "BC-FIRE":
                        bc.append((comp+': ' +name))
                    case other:
                        ...

        print("[*]", list(dc))
        print("[*]", list(bc))


    def multiple_days_off(self):
        sl = []
        for value in self.data.values():
            is_field = self._field_personnel(value)


            if value["paycode"] == "SL" :

                if value["detail_code"] != 'Not listed' and is_field:
                    sl.append((value["name"], value["paycode"], value["detail_code"]))
        return sl
    
        
    def __call__(self):
        chiefs = self._on_duty_chiefs()
        data = self._paycode_count()
        multi_day = self.multiple_days_off()

        return itertools.chain(data,multi_day)




















    def to_excel(self):
        wb = Workbook()
        ws = wb.active

        ws.append(["SHIFT", "COMPANY", "EID", "RANK", "LAST_NAME", "FIRST_NAME", "GROUPS"])
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
                
                entry= [shift, str(comp), d["eid"], d["rank"], d["last_name"], d["first_name"], d["groups"]]
            

                print(shift, comp, d["eid"], d["rank"], d["last_name"], d["first_name"], d["groups"], sep=", ")

        #wb.save("/Users/jessemeekins/Desktop/Person_export.xlsx")
        wb.close()