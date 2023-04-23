#%%
from typing import Type
from dataclasses import dataclass
from functools import singledispatch

from dataparser import DataParser, XmlDataParser
from importer import XmlImporter, Importer
from datafilters import (
    ReportType, AlsCompanyReport,
    AssignmentReport, FullRosterReport,
    PayCodes
)
from mapper import (
    DataFieldsMapper, XmlAlsFieldsMap,
    FullExportFieldsMapper, AssignmentExportMapper,
)
from exporter import ReportFactory, DailyNumbersReport
from file_path_manager import get_file_path
from datetime_formatter import DateTimeFormatter


@dataclass
class FileCompose:
    importer: Importer
    mapper: DataFieldsMapper
    parser: DataParser
    report: ReportType


@dataclass
class FileFactoryExporter:
    importer_class: Type[Importer]
    mapper_class: Type[DataFieldsMapper]
    parser_class: Type[DataParser]
    report_class: Type[ReportType]


    def __call__(self, arg) -> FileCompose:
        file_path_obj = get_file_path(arg)
        importer = self.importer_class(file_path_obj)
        raw_file_data = importer.importer()
        parser = self.parser_class(raw_file_data, self.mapper_class())
        report = self.report_class(parser())
        
        return report()


FACTORY = {
    "ALS": FileFactoryExporter(XmlImporter, XmlAlsFieldsMap, XmlDataParser, AlsCompanyReport),
    "FULL": FileFactoryExporter(XmlImporter, FullExportFieldsMapper, XmlDataParser, FullRosterReport),
    "PPL": FileFactoryExporter(XmlImporter, AssignmentExportMapper, XmlDataParser, AssignmentReport),
    "PAYCODES" : FileFactoryExporter(XmlImporter, FullExportFieldsMapper, XmlDataParser, PayCodes),
}


now = DateTimeFormatter.local_timestamp()


def factory_builder(arg: str, *args, **kwargs) -> dict:
    f = get_file_path(arg)
    if not f:
        raise ValueError("Invalid argument provided.")
    return FACTORY[arg]


def main(arg: str, export_to_excel=False, *args, **kwargs) -> None:
    data = factory_builder(arg)
    if data:
        # Single dispatch for error handling alternative
        @singledispatch
        def proccess_data(data:dict):
            for _, item in data(arg).items():
                try:
                    for k , v in item.items():
                        print(f"[*] {k}: {v}")
                except AttributeError:
                    _list = list()
                    for s in item:
                        _list.append(s)
                    print(_,sorted(_list))             
                except Exception as e:
                    print(e)
                    print("[*] Unable to proccess data...") 
        
        @proccess_data.register(str)
        def _(data:str):
            print(data)

        @proccess_data.register(list)
        def _(data: list):
            for d in data:
                print(d)
        
        proccess_data(data)

    if export_to_excel:
        print("[*] Exporting to file...")
        daily_number_report = DailyNumbersReport(data(arg))
        daily_number_report.generate_report("/Users/jessemeekins/Desktop/daily_number_report.xlsx")

if __name__ == "__main__":
    main("PAYCODES")
