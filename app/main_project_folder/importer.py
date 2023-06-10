"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
from main_project_folder.file_path_manager import DefinedFilePaths
import json
import csv


class Importer(ABC):
    def __init__(self, file_path_obj: DefinedFilePaths) -> None:
        self.file_path_object = file_path_obj()

    @abstractmethod
    def importer():
        pass

class XmlImporter(Importer):
    """Initialized with DefinedFilePaths object"""
        
    def importer(self):
        """Locate the file to parse and return xml.etree.ElementTree obj"""
        tree = ET.parse(str(self.file_path_object))
        root = tree.getroot()
        return root

class JsonFileImporter(Importer):
    """Initialize a JSON file importer object"""
    def importer(self):
        file_contents: dict() = json.loads(self.file_path_object)
        return file_contents


        
        


