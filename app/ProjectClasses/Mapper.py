from abc import ABC, abstractmethod

class DataFieldsMapper(ABC):
    """Data Field Mappers for Various reports"""
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def field_mapper(self, record) -> dict:
        ...

class XmlAlsFieldsMap(DataFieldsMapper):
    def field_mapper(self, record) -> dict:
        try:
            try:
                profile_specialties = record.find('RscFormulaIDCh').text
            except:
                profile_specialties = 'Uknown'
            
            rank_of_person = record.find('PosJobAbrvCh').text
            current_company = record.find('PUnitAbrvCh').text
            shift_start = record.find('StaffingStartDt').text
            shift_end = record.find('ShiftEndDt').text

            payload = {
                'rank_of_person':rank_of_person, 
                'profile_specialties':profile_specialties, 
                'current_company':current_company, 
                'shift_start_and_end': (shift_start, shift_end)
            }    
            return payload
        except Exception as e:
            pass


class FullEXportFieldsMapper(DataFieldsMapper):
    def field_mapper(self, record) -> dict:
        try:
            shift = record.find('ShiftAbrvCh').text
            is_working = record.find('WstatIsWorkingGm').text
            shift_start = record.find('StaffingStartDt').text
            shift_end = record.find('ShiftEndDt').text
            region =record.find('RegionAbrvCh').text
            station =record.find('StationAbrvCh').text
            unit = record.find('PUnitAbrvCh').text
            rank = record.find('PosJobAbrvCh').text
            shift_start = record.find('StaffingStartDt').text
            shift_end = record.find('ShiftEndDt').text
            paycode = record.find('WstatAbrvCh').text
            try:
                specialties = record.find('RscFormulaIDCh').text
            except:
                specialties = 'Uknown'
            
            payload = {
                "shift": shift,
                "is_working": is_working,
                'shift_start_and_end': (shift_start, shift_end),
                "region": region,
                "station": station,
                "unit": unit,
                "rank": rank,
                "paycode": paycode,
                "specialties": specialties
            }
            return payload
        except:
            pass


