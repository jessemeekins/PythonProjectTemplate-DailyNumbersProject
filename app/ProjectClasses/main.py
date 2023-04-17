
#%%
"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""

from typing import Type
from dataclasses import dataclass

from dataparser import (
    DataParser,
    XmlDataParser)
from importer import (
    XmlImporter,
    Importer,
    )
from datafilters import (
    ReportTypeClass,
    AlsCompanyReport,
    AssignmentReport,
    FullRosterReport,
    )
from mapper import (
    DataFieldsMapper, 
    XmlAlsFieldsMap, 
    FullExportFieldsMapper, 
    AssignmentExportMapper
    )
from filepaths import FILE_PATH_FACTORY
from dateandtimeclass import DateTimeFormatter

now = DateTimeFormatter.local_timestamp()


@dataclass
class FileCompose:
    importer: Importer
    mapper: DataFieldsMapper
    parser: DataParser
    report: ReportTypeClass

@dataclass
class FileFactoryExporter:
    importer_class: Type[Importer]
    mapper_class: Type[DataFieldsMapper]
    parser_class: Type[DataParser]
    report_class: Type[ReportTypeClass]

    def __call__(self) -> FileCompose:
        return FileCompose(
            self.importer_class,
            self.mapper_class,
            self.parser_class,
            self.report_class
        )

FACTORY = {
    "ALS" : FileFactoryExporter(XmlImporter,XmlAlsFieldsMap, XmlDataParser, AlsCompanyReport),
    "FULL" : FileFactoryExporter(XmlImporter, FullExportFieldsMapper, XmlDataParser, FullRosterReport),
    "PPL": FileFactoryExporter(XmlImporter,AssignmentExportMapper, XmlDataParser, AssignmentReport)
    }

def factory_builder(arg: str, *args, **kwargs) -> dict :
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
    # Predefined report class object
    report = conf.report_class
    # File data after XML has been parsed into workable data 
    raw_file_data = importer(path, file).importer()
    # File parser takes in raw data and filters throught the mapper class
    full_data = parser(raw_file_data, mapper())
    #full_data = report(full_data)
    return report(full_data())


def main(arg: str, verbose=False, *args, **kwargs) -> None:
    
    _data = factory_builder(arg)
    for k in _data():
        print(k)
        

    print(f"[*] Proccessing complete: {now}")
    if verbose:
        print("[*]")
        
if __name__ == "__main__":
    main("FULL")


