"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""
from abc import ABC, abstractmethod
from mapper import DataFieldsMapper

class DataParser(ABC):
    def __init__(self) -> None:
        ...
    @abstractmethod
    def _parser_format(self):
        ...

class XmlDataParser:
    """Loops though each record of records in a XML file, 'key_tag' set to record,
    the internal file tag for each individual record in telestaff in a given report"""
    def __init__(self, data, mapper: DataFieldsMapper, key_tag='Record') -> None:
        self.data = data
        self.mapper: DataFieldsMapper = mapper
        self.key = key_tag


    def _parser_format(self) -> dict:
        """Takes in the XML.Tree from the XMLImporter Class and loops through the records"""
        records_dict = dict()
        for i, child in enumerate(self.data.iter(self.key)):
            record = self.mapper.field_mapper(child)
            records_dict[i] = record
        return records_dict

    def __call__(self) -> dict:
        return self._parser_format()
