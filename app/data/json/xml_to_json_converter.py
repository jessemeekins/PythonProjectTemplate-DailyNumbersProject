#%%
import json
import xmltodict
from datetime import datetime, timedelta


def shift_start_end_adjust(i=0) -> str:
    today = datetime.today() - timedelta(days=i,hours=7)
    formatted_time = datetime.strftime(today, "%Y-%m-%d")
    return formatted_time 
        

def xml_to_json_converter(xml_file_path: str, json_file_path: str) -> None:
    with open(xml_file_path) as xml_file:
        xml_data = xml_file.read()
        parsed_data = xmltodict.parse(xml_data)
        json_data = json.dumps(parsed_data)

    with open(json_file_path, 'w') as json_file:
        json_file.write(json_data)

    print("[*] Conversion complete!")

adjusted_shift_date = shift_start_end_adjust()

exports=  {
    "full" : {
        "source" : f"/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/Full Roster Export Hourly{adjusted_shift_date}_{adjusted_shift_date}.xml",
        "destination" : f"/Users/jessemeekins/Documents/VS_CODE/mfd-numbers-nextjs/public/full_roster.json"
        },
    "full_hist" : {
        "source" : f"/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/Full Roster Export Hourly{adjusted_shift_date}_{adjusted_shift_date}.xml",
        "destination" : f"/Users/jessemeekins/Documents/VS_CODE/mfd-numbers-nextjs/public/full_roster_{adjusted_shift_date}.json"
        },
    "assign" : {
        "source" : f"/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/full_assignment.xml",
        "destination" : f"/Users/jessemeekins/Documents/VS_CODE/mfd-react/public/full_assignment.json"
    },
    "server_test" : {
        "source" : f"/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/Full Roster Export Hourly{adjusted_shift_date}_{adjusted_shift_date}.xml",
        "destination" : f"/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/json/full_roster.json"
    }
}

def main(*reports:str):
    for report in reports:    
        file_path = exports.get(report)  

        xml_to_json_converter(file_path["source"], file_path["destination"])

        with open(file_path["destination"]) as f:
            data = json.load(f)

        if report == "full":
            records_list = data["DataRoot"]["Data"]["Records"]["Record"]
        if report == "assign":
            records_list = data["Data"]["Records"]["Record"]

        with open(file_path["destination"], 'w') as f:
            json.dump(records_list, f)

if __name__ == "__main__":
    main("assign", "full", "full_hist", "server_test")
    
    
