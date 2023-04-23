"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
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
        return payload
      

class XmlAlsFieldsMap(DataFieldsMapper):
    def field_mapper(self, record) -> list[tuple]:
        fields = [
            ("specialties" ,'RscFormulaIDCh'),
            ("region", 'RegionAbrvCh'),
            ("station", 'StationAbrvCh'),
            ("unit", 'PUnitAbrvCh'),
            ("rank", 'PosJobAbrvCh'),
            ("shift_start", 'StaffingStartDt'),
            ("shift_end", 'ShiftEndDt'),
            ("is_working", 'WstatIsWorkingGm'),
        ]
        return super().__call__(record=record, fields=fields)
            

class FullExportFieldsMapper(DataFieldsMapper):
    def field_mapper(self, record) -> list[tuple]:
        fields = [
            ("name", "RscMasterNameCh"),
            ("is_working", 'WstatIsWorkingGm'),
            ("shift", 'ShiftAbrvCh'),
            ("paycode" , 'WstatAbrvCh'),
            ('detail_code', 'StaffingDetailCh'),
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
    
class NewMap(DataFieldsMapper):
    def field_mapper(self) -> list[tuple]:
        fields = {
            
        }