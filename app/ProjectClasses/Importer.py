"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

class Importer(ABC):
    def __init__(self) -> None:
        ...

    @abstractmethod
    def importer():
        ...

class XmlImporter(Importer):
    """Initialized with filepath: str and filename: str"""
    def __init__(self,filepath: str, filename: str) -> None:
        self.filepath = filepath
        self.filename = filename
      
    def importer(self): 
        """Located the file to parse and return xml.etree.ElementTree obj"""
        tree = ET.parse(f"{self.filepath}{self.filename}")
        root = tree.getroot()
        return root
    