#%%
from collections import namedtuple
from typing import Protocol
from ProjectClasses.DataFilters import ALS
from ProjectClasses.DataParser import DataParser
from ProjectClasses.Importer import XmlImporter
from ProjectClasses.DateAndTimeClass import DateTimeFormatter
from ProjectClasses.Mapper import XmlAlsFieldsMap
from ProjectClasses.Exporter import JSONFormatExporter

formatted_time = DateTimeFormatter.shift_start_end_adjust()

class FileLocation(namedtuple("File", ['filepath', 'filename'])):    
    ...

class InstantiateClassParser(Protocol):
    def instantiate(class_to_instantiate: object, file_named_tuple: FileLocation) -> dict:
        return class_to_instantiate(file_named_tuple.filepath, file_named_tuple.filename)
    
class XmlFileFactory:
    def instantiate(file_named_tuple) -> dict:
        return XmlImporter(file_named_tuple)


registered_factory = {
    "DEV": XmlImporter
}

configuration = {
    "DEV" : {
        "filepath": "/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/",
        "filename": f'ROS11 MFD{formatted_time}.xml'} 
    }

def file_config(arg: str) -> tuple:
    file_info = configuration.get(arg)
    return FileLocation(file_info["filepath"], file_info["filename"])

def register_factory(arg:str) -> object:
    return registered_factory.get(arg)

def main(arg: str,verbose=False) -> None:

    fac = registered_factory.get(arg)
    file = file_config(arg)

    instantiated_class = fac(file.filepath, file.filename)
    raw_file_data = instantiated_class.importer()
    parsed_data = DataParser(raw_file_data, XmlAlsFieldsMap).xml_into_dictionary()
    test = ALS(parsed_data)
    d = test.list_als_companies()
    complete_time = DateTimeFormatter.local_timestamp()
    print(f"[*] Proccessing complete: {complete_time}")
    if verbose:
        print("[*]", d)

if __name__ == "__main__":
 
    main("DEV",verbose=True)

