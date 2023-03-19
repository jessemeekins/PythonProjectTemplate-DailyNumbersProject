#%%
import logging
from abc import ABC, abstractmethod
from data.FileTypeFormatter import Formatters

log = logging.Logger('.//default_logger.log')

class DataUploaderClass(ABC):
    @abstractmethod
    def file_importer(self):
        """retrieve file based on file type"""

    @abstractmethod
    def load_data(self):
        """upload file into program ready for logic"""


class XMLFileUploader(DataUploaderClass):
    def file_importer(self) -> str:
        file_name = Formatters.XMLFormatterClass.XML_file_name()
        return file_name
        
    def load_data(self):
        return Formatters.XMLFormatterClass.XML_file_data()
 

class XLSXFileUploader(DataUploaderClass):
    def file_importer(self) -> str:
        file_name = Formatters.XLSXFormatterClass.XLSX_importer()
        return file_name
    
    def load_data(self):
        ...

class PatternClass(ABC):
    def __init__(self, uploader: DataUploaderClass) -> None:
        self.uploader = uploader

    def __repr__(self) -> str:
        return f"{self.uploader}"
        
    @abstractmethod
    def function_1(self):
        """Initilized method_1"""

    @abstractmethod
    def function_2(self):
        """Initilized method_2"""

    def execute(self): ...


class PatternClassMethod_1(PatternClass):
    def function_1(self, arg: dict) -> list:
        if arg:
            ALS_record = list(map(lambda x: x["company"] ,filter(lambda x: x["position"] =='1.1', arg.values())))
            print("[*] PatternClassMethod_1::function_1 executed")
            return ALS_record
        else: ...
     
    def function_2(self, arg: list) -> None: 
        if arg:
            print("[*] Recieved List")
            l = len(list(set(arg)))
            filtered_list = list(filter(lambda x: "BC" not in x, filter(lambda x: "EU" not in x, arg)))
            print("[*] Count:" , len(list(filtered_list)) )
            print(sorted(filtered_list))

        else: ... 

class PatternClassMethod_2(PatternClass):
    def function_1(self, arg: None) -> None:
        if arg:
            print("[*] PatternClassMethod_2::function_1 executed")
        else: ...
    def function_2(self, arg: None) -> None:
        if arg:
            print("[*] PatternClassMethod_2::function_2 executed")
        else: ...


def execute(method:str) -> PatternClass:
    registered_methods = {
        "one": PatternClassMethod_1(XMLFileUploader()),
        "two": PatternClassMethod_2(XLSXFileUploader())
    }
    choice = registered_methods.get(method, None)
    return choice


def main(method:str) -> None:
    class_pattern = execute(method=method)
    file = class_pattern.uploader.file_importer()
    source = class_pattern.uploader.load_data()
    parsed_data = class_pattern.function_1(source)
    data = class_pattern.function_2(parsed_data)
    complete_time = Formatters.DatetimeTimeFormatter.local_timestamp()
    print(f"[{complete_time}] Execution completed on file name :: {file}")


if __name__ == "__main__":
    choice = input("Method choice ('one', 'two')?")
    main(method=choice)

