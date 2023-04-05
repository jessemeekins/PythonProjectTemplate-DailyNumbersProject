from abc import ABC, abstractmethod

class DataFieldsMapper(ABC):
    """Data Field Mappers for Various reports"""

    @abstractmethod
    def field_mapper(record) -> dict:
        ...

class XmlAlsFieldsMap(DataFieldsMapper):
    def field_mapper(record) -> dict:
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
