#%%
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

from typing import Type
from dataclasses import dataclass

from importer import XmlImporter
from dataparser import DataParser
from datafilters import PayCodeFilters
from dateandtimeclass import DateTimeFormatter
from mapper import (
    DataFieldsMapper, 
    XmlAlsFieldsMap, 
    FullExportFieldsMapper, 
    AssignmentExportMapper
)
from filepaths import FILE_PATH_FACTORY


@dataclass
class FileCompose:
    importer: XmlImporter
    mapper: DataFieldsMapper
    parser: DataParser

@dataclass
class FileFactoryExporter:
    importer_class: Type[XmlImporter]
    mapper_class: Type[DataFieldsMapper]
    parser_class: Type[DataParser]

    def __call__(self) -> FileCompose:
        return FileCompose(
            self.importer_class,
            self.mapper_class,
            self.parser_class
        )

FACTORY = {
    "ALS" : FileFactoryExporter(XmlImporter,XmlAlsFieldsMap, DataParser),
    "FULL" : FileFactoryExporter(XmlImporter, FullExportFieldsMapper, DataParser),
    "PPL": FileFactoryExporter(XmlImporter,AssignmentExportMapper, DataParser)
    }

def factory_builder(arg: str) -> dict:
    """Initializes the factory classes and sets file paths"""
    # function located in filepath.py
    # Has __call__, will concat into complete file path ex. ->f()
    f = FILE_PATH_FACTORY[arg]
    path = f.filepath
    file = f.filename
    # Dict listed above
    conf = FACTORY[arg]
    # Importer class gets file path and name and parses xml format
    importer = conf.importer_class
    # Loops through formated file and "filters" through a predefined field mapping
    parser = conf.parser_class
    # Predefined field mapping based on report type and need
    mapper = conf.mapper_class
    
    # File data after XML has been parsed into workable data 
    raw_file_data = importer(path, file).importer()
    # File parser takes in raw data and filters throught the mapper class
    full_data = parser(raw_file_data, mapper())
    # within parser.py we now add all data to a python dict
    full_data.xml_into_dictionary()

def main(arg: str, verbose=False) -> None:
    
    factory_builder(arg)
    #### TO DO #####
    # CREATE Factory patterns for data proccessing 

    complete_time = DateTimeFormatter.local_timestamp()
    print(f"[*] Proccessing complete: {complete_time}")
    if verbose:
        print("[*]")
        
if __name__ == "__main__":
    main("ALS")


