#%%
import json
import xmltodict
from typing import Any, Dict
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path

def shift_start_end_adjust(i=0) -> str:
    today = datetime.today() - timedelta(days=i,hours=7)
    return today.strftime("%Y-%m-%d")

class RecordsFilter(ABC):
    def __init__(self, params: Dict[str, Any], file: str) -> None:
       """initialize the class"""
       self.file = file
       self.params = params

    def _json_data(self) -> dict:
        """parse the XML file into python dict format and return"""
        with open(self.file, 'r') as f:
            return xmltodict.parse(f.read())

    def _file_path_manager(self, filename: str, directory: Path, sub_directory: str = None) -> str:
        """function to return the desired file path for the json file to be exported to"""
        directory_path = directory / sub_directory if sub_directory else directory
        if Path.exists(directory_path):
            return str(directory_path / filename)
        else:
            return str(Path.cwd() / filename)
        
    def _creates_json_file(self) -> None:
        json_data = self.filter_records()
        filepath = self._file_path_manager(
            filename=self.params["filename"], 
            directory=self.params["directory"], 
            sub_directory=self.params.get("sub_directory")  # using .get() in case "sub_directory" is not in params
        )
        with open(filepath, 'w') as json_file:
            json.dump(json_data, json_file)

    @abstractmethod
    def filter_records(self) -> dict:
        """filter record data from XML file"""
        
    @abstractmethod
    def __call__(self) -> Any:
        """want to make each child callable for factory pattern usage"""

class WorkingTypeRecords(RecordsFilter):
    def filter_records(self) -> list[dict]:
        records = list()
        data = self._json_data()
        records_list = data["DataRoot"]["Data"]["Records"]["Record"]
        for record in records_list:
            if record["WstatIsWorkingGm"] == self.params['on_duty']:
                records.append(record)
        return records

    def __call__(self) -> None:
        self._creates_json_file()

if __name__ == "__main__":
    adjusted_shift_date = shift_start_end_adjust()
    current_roster = f"/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/Full Roster Export Hourly{adjusted_shift_date}_{adjusted_shift_date}.xml"

    arg_dict ={
        "OnDutyRecords" : {
            "filename": "onDutyRecords.json",
            "directory": Path("/var/www/html/mfd/api/v1"),
            "sub_directory": "rosters",
            "on_duty": "true"
        },
        "OffDutyRecords" : {
            "filename": "offDutyRecords.json",
            "directory": Path("/var/www/html/mfd/api/v1"),
            "sub_directory": "rosters",
            "on_duty": "false"
        },
    }

    for param, args in arg_dict.items():
        worker = WorkingTypeRecords(args, file=current_roster)
        worker()
