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

