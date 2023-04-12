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

