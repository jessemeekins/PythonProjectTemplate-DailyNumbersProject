"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""

from typing import Type
from dataclasses import dataclass
from main_project_folder.datetime_formatter import DateTimeFormatter
from pathlib import Path

ADJUSTED_FILE_DATE = DateTimeFormatter.shift_start_end_adjust()


@dataclass
class DefinedFilePaths:
    filepath: str
    filename: str

    def __str__(self):
        return str(Path(self.filepath) / self.filename)


@dataclass
class FilePathFactory:
    filepath: Type[DefinedFilePaths]
    filename: Type[DefinedFilePaths]

    def __call__(self) -> DefinedFilePaths:
        return DefinedFilePaths(self.filepath, self.filename).__str__()


FILE_PATH_FACTORY = {
    "JSON": FilePathFactory(
        Path("/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/json/"),
             f"full_roster_export{ADJUSTED_FILE_DATE}.json "
    ),
    "ALS": FilePathFactory(
        Path("/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/"),
        f"ROS11 MFD{ADJUSTED_FILE_DATE}.xml"
    ),
    "PPL": FilePathFactory(
        Path("/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/"),
        "full_assignment.xml"
    ),
    "FULL": FilePathFactory(
        Path("/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/"),
        f'Full Roster Export Hourly{ADJUSTED_FILE_DATE}_{ADJUSTED_FILE_DATE}.xml'
    ),
    "PAYCODES": FilePathFactory(
        Path("/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/"),
        f'Full Roster Export Hourly{ADJUSTED_FILE_DATE}_{ADJUSTED_FILE_DATE}.xml'
    ),
    "ASSIGN": FilePathFactory(
        Path("/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/"),
        'full_assignment.csv'
    ),
}


def get_file_path(arg: str) -> DefinedFilePaths:
    
    try:
        return FILE_PATH_FACTORY[arg]
    except KeyError:
        return FILE_PATH_FACTORY["FULL"]

