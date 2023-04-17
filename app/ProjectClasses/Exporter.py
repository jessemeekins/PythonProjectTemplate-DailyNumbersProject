"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""

from abc import ABC, abstractmethod
import openpyxl
import json


class DataExporter(ABC):
    def __init__(self, data) -> None:
        self.data = data
    
    @abstractmethod
    def export(self):
        """Do the Export"""


class DictionaryFormatExporter(DataExporter):
    def export(self) -> dict:
        return dict(self.data)
    

class JSONFormatExporter(DataExporter):
    def export(self):
        return json.dumps(self.data)
    
class ExcelExporter():
    ...
    
    