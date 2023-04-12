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

from abc import ABC, abstractmethod

class DataFieldsMapper(ABC):
    """Data Field Mappers for Various reports"""
    def __init__(self) -> None:
        ...

    @abstractmethod
    def field_mapper(self) -> list[tuple]:
        """Returns mapping to XML file in tuple format"""
        ...

    def __call__(self, record, fields) -> dict:
        """Maps list of tuples to fields in XML file and handles errors and special cases"""
        payload = dict()
        for field in fields:
            try:
                data = record.find(field[1]).text
                if data:
                    if field[0] == 'specialities':
                        spec_list = data.split(',')
                        payload[field[0]] = spec_list
                    else:
                        payload[field[0]] = data
                else:
                    payload[field[0]] = "Not listed"
            except:
                payload[field[0]] = "Not listed"
        print(payload)
        return payload
      

class XmlAlsFieldsMap(DataFieldsMapper):
    def field_mapper(self, record) -> list[tuple]:
        fields = [
            ("specialties" ,'RscFormulaIDCh'),
            ("rank", 'PosJobAbrvCh'),
            ("company", 'PUnitAbrvCh'),
            ("shift_start", 'StaffingStartDt'),
            ("shift_end", 'ShiftEndDt'),
        ]
        return super().__call__(record=record, fields=fields)
            

class FullExportFieldsMapper(DataFieldsMapper):
    def field_mapper(self, record) -> list[tuple]:
        fields = [
            ("is_working", 'WstatIsWorkingGm'),
            ("shift", 'ShiftAbrvCh'),
            ("paycode" , 'WstatAbrvCh'),
            ("region", 'RegionAbrvCh'),
            ("station", 'StationAbrvCh'),
            ("unit", 'PUnitAbrvCh'),
            ("rank", 'PosJobAbrvCh'),
            ("shift_start", 'StaffingStartDt'),
            ("shift_end", 'ShiftEndDt'),
            ("specialties",'RscFormulaIDCh'),
        ]

        return super().__call__(record=record, fields=fields)
        

class AssignmentExportMapper(DataFieldsMapper):
    def field_mapper(self, record) -> list[tuple]:
        fields = [
            ("eid", 'RscMaster_EmployeeID_Ch'),
            ("rank", 'Job_Abrv_Ch'),
            ("full_rank", 'Rsc_Desc_Ch'),
            ("last_name" ,'RscMaster_LName_Ch'),
            ("first_name", 'RscMaster_FName_Ch'),
            ("specialities", 'Spec_Skill_In'),
            ("groups", 'Group_Skill_In'),
            ("pay_info", "PayInfo_Name_Ch")
        ]
        
        return super().__call__(record=record, fields=fields)