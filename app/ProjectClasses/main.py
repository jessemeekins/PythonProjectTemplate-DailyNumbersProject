#%%
from typing import Type
from dataclasses import dataclass

from dataparser import DataParser, XmlDataParser
from importer import XmlImporter, Importer
from datafilters import (
    ReportTypeClass, AlsCompanyReport,
    AssignmentReport, FullRosterReport,
)
from mapper import (
    DataFieldsMapper, XmlAlsFieldsMap,
    FullExportFieldsMapper, AssignmentExportMapper,
)
from exporter import ReportFactory, DailyNumbersReport
from filepaths import FILE_PATH_FACTORY
from dateandtimeclass import DateTimeFormatter


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


    def __call__(self, arg) -> FileCompose:
        importer = self.importer_class(FILE_PATH_FACTORY[arg].filepath, FILE_PATH_FACTORY[arg].filename, )
        raw_file_data = importer.importer()
        parser = self.parser_class(raw_file_data, self.mapper_class())
        report = self.report_class(parser())
        
        return report()


FACTORY = {
    "ALS": FileFactoryExporter(XmlImporter, XmlAlsFieldsMap, XmlDataParser, AlsCompanyReport),
    "FULL": FileFactoryExporter(XmlImporter, FullExportFieldsMapper, XmlDataParser, FullRosterReport),
    "PPL": FileFactoryExporter(XmlImporter, AssignmentExportMapper, XmlDataParser, AssignmentReport),
}


now = DateTimeFormatter.local_timestamp()


def factory_builder(arg: str, *args, **kwargs) -> dict:
    f = FILE_PATH_FACTORY.get(arg)
    if not f:
        raise ValueError("Invalid argument provided.")
    return FACTORY[arg]


def main(arg: str, verbose=False, *args, **kwargs) -> None:
    _data = factory_builder(arg)
    if _data:
        for _, item in _data(arg).items():
            for k , v in item.items():
                print(f"[*] {k}: {v}")
    
    if verbose:
    
        print("[*] Exporting to file...")
        daily_number_report = DailyNumbersReport(_data(arg))
        daily_number_report.generate_report("/Users/jessemeekins/Desktop/daily_number_report.xlsx")

if __name__ == "__main__":
    main("FULL", True)
