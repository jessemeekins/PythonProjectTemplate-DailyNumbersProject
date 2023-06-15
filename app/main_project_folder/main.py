#%%
import json
from typing import Type
from dataclasses import dataclass

from main_project_folder.dataparser import DataParser, XmlDataParser
from main_project_folder.importer import XmlImporter, Importer
from main_project_folder.report_type import (
    ReportType, AlsCompanyReport,
    AssignmentReport, FullRosterReport,
    PayCodes, OnDutyChiefs, ComplimentReport,
    RankCounts, CurrentShift, DetailedPersonnel,
    FormulaIDAudit, RosterAudit, OvertimeAudit,
    PositionReport
)
from main_project_folder.mapper import (
    DataFieldsMapper, XmlAlsFieldsMap,
    FullExportFieldsMapper, AssignmentExportMapper,
)
from main_project_folder.exporter import ReportFactory, DailyNumbersReport
from main_project_folder.file_path_manager import get_file_path
from main_project_folder.datetime_formatter import DateTimeFormatter


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
    "CHIEFS" : FileFactoryExporter(XmlImporter, FullExportFieldsMapper, XmlDataParser, OnDutyChiefs),
    "COMP" : FileFactoryExporter(XmlImporter, FullExportFieldsMapper, XmlDataParser, ComplimentReport),
    "RANK" : FileFactoryExporter(XmlImporter, FullExportFieldsMapper, XmlDataParser, RankCounts),
    "SHIFT" : FileFactoryExporter(XmlImporter, FullExportFieldsMapper, XmlDataParser, CurrentShift),
    "DETAILED" : FileFactoryExporter(XmlImporter, FullExportFieldsMapper, XmlDataParser, DetailedPersonnel ),
    "AUDIT" : FileFactoryExporter(XmlImporter, AssignmentExportMapper, XmlDataParser, FormulaIDAudit),
    "DUP" : FileFactoryExporter(XmlImporter, FullExportFieldsMapper, XmlDataParser, RosterAudit),
    "OT" : FileFactoryExporter(XmlImporter, FullExportFieldsMapper, XmlDataParser, OvertimeAudit),
    "POS" : FileFactoryExporter(XmlImporter, XmlAlsFieldsMap, XmlDataParser, PositionReport),

}

now = DateTimeFormatter.local_timestamp()
today = DateTimeFormatter.shift_start_end_adjust()

def factory_builder(arg: str, *args, **kwargs) -> dict:
    f = get_file_path(arg)
    if not f:
        raise ValueError("Invalid argument provided.")
    return FACTORY[arg]

def proccess_data(data: dict):
    if isinstance(data, dict):
        proccessed_data = dict()
        for _, item in data.items():
            try:
                for k, v in item.items():
                    proccessed_data[k] = v
            except AttributeError:
                proccessed_data = item
        return proccessed_data
    else:
        print(f"Unable to process data: {data}")
        return None

def main(arg: str, export_to_excel=False, export_to_json=False, *args, **kwargs) -> None:
    data = factory_builder(arg)(arg)
    if data:       
        proccessed_data = proccess_data(data)
        if export_to_excel:
            print("[*] Exporting to file...")
            daily_number_report = DailyNumbersReport(data(arg))
            daily_number_report.generate_report("/Users/jessemeekins/Desktop/daily_number_report.xlsx")
        if export_to_json:
            AlsCompanyReport.json_als_companies()
    else:
        proccessed_data = None
    return proccessed_data

if __name__ == "__main__":
    main("ALS", export_to_json=False, export_to_excel=False)
