"""
Copyright (c) 2023 Jesse Meekins

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import datetime
from openpyxl import Workbook

class DataFilters:
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
        return _data["shift_start_and_end"]

    @staticmethod
    def _currently_working(tupled_times: tuple[datetime,datetime]) -> bool:
        now = datetime.now()
        return now > tupled_times[0] and now < tupled_times[1]

    @staticmethod
    def _paramedic(data:dict) -> bool:
        return data["rank_of_person"] == "FFP" or "EMTP" in data["profile_specialties"]       
        
    @staticmethod
    def _company_identifier(data:dict) -> str:
        return data["current_company"]
    
    @staticmethod
    def _company_abrev_first_two_letters(data:str):
        return data["current_company"][0:2]
    
    @staticmethod
    def _paycode(data:dict) -> str:
        return data["paycode"]
    
    @staticmethod
    def _shift(data:dict) -> str:
        return data["shift"]


class ALS(DataFilters):
    def __init__(self, data: dict) -> None:
        self.data = data
    
    def list_als_companies(self) -> dict:
        """Mini Procotcal method for finding ALS companies in service"""
        
        als_dict = dict()
        for i, record in enumerate(self.data.values()):
            # gets tuple with string reprs of datetime from file
            t_times = self._get_tupled_times(record)
            # reformats ISO 8601 into datetime objects for further comparisems
            formatted_times = self.ISO_8601_reformatter(t_times)
            #performs check to see if recrods is within a certain timeframe
            on_duty = self._currently_working(formatted_times)
            # checks to see if record is == to a paramedic
            paramedic = self._paramedic(record)
            # Get the company CAD abrv
            comp = self._company_identifier(record)

            # Checking the dictionary for company abrv 
            if on_duty and paramedic:
                # retrieves a string repr of the fire companies abrv
                als_dict[comp] = {"ALS": True}
            else:
                ...
        return als_dict
    
    def als_count(self) -> int:
        comp = self.list_als_companies()
        fire_comp = [c for c in comp.keys() if "PU" in c or "TR" in c or "RC" in c]
        return len(fire_comp)

    
class PayCodeFilters(DataFilters):
    def __init__(self, data) -> None:
        self.data: dict = data

    def all_records(self) -> dict:
        return self.data
            
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
                comp = [c for c in d["specialities"] if "PU" in c or "TR" in c or "RC" in c or "QT" in c or "BC" in c]
                if comp:
                    comp = comp[0]
                else:
                    comp = "No company listed"
                
                entry= [shift, str(comp), d["eid"], d["rank"], d["last_name"], d["first_name"], d["groups"]]
                ws.append(entry)

                print(shift, comp, d["eid"], d["rank"], d["last_name"], d["first_name"], d["groups"], sep=", ")

        #wb.save("/Users/jessemeekins/Desktop/Person_export.xlsx")
        wb.close()