"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
from file_path_manager import DefinedFilePaths


class Importer(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def importer():
        pass


class XmlImporter(Importer):
    """Initialized with DefinedFilePaths object"""

    def __init__(self, file_path_obj: DefinedFilePaths) -> None:
        self.file_path_obj = file_path_obj()

    def importer(self):
        """Locate the file to parse and return xml.etree.ElementTree obj"""
        tree = ET.parse(str(self.file_path_obj))
        root = tree.getroot()
        return root

