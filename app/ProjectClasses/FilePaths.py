"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""
#%%
from typing import Type
from dataclasses import dataclass
from dateandtimeclass import DateTimeFormatter

ADJUSTED_FILE_DATE = DateTimeFormatter.shift_start_end_adjust()

@dataclass
class DefinedFilePaths:
    filepath: str
    filename: str
    
    def __str__(self):
        return f"{self.filepath}{self.filename}"    
    
@dataclass
class FilePathFactory:
    filepath: Type[DefinedFilePaths]
    filename: Type[DefinedFilePaths]

    def __call__(self) -> DefinedFilePaths:
        return DefinedFilePaths(self.filepath, self.filename).__str__()


FILE_PATH_FACTORY = {
    "ALS": FilePathFactory("/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/",f"ROS11 MFD{ADJUSTED_FILE_DATE}.xml"),
    "PPL": FilePathFactory("/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/","person-export-.xml"),
    "FULL": FilePathFactory("/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/","Full Roster Export Hourly.xml")
}

def get_file_path(arg: str) -> DefinedFilePaths:
    return FILE_PATH_FACTORY[arg]

