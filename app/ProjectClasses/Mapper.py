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


