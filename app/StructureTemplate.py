#%%
import logging
from abc import ABC, abstractmethod
from data.FileTypeFormatter import Formatters

log = logging.Logger('.//default_logger.log')

class DataUploaderClass(ABC):
    @abstractmethod
    def file_importer(self):
        """file importer"""


class XMLFileUploader(DataUploaderClass):
    def file_importer(self) -> str:
        file_name = Formatters.XMLFormatterClass.XML_file_name()

        return file_name, Formatters.XMLFormatterClass.XML_file_data() 


class ParTelestaffFileUploader(DataUploaderClass):
    def file_importer(self) -> str:
        
        file_name = Formatters.XLSXFormatterClass.XLSX_importer()
        return file_name, '[*]'
    

class PatternClass(ABC):
    def __init__(self, uploader: DataUploaderClass) -> None:
        self.uploader = uploader

    def __repr__(self) -> str:
        return f"{self.uploader}"
        
    @abstractmethod
    def class_function(self, *args):
        """Initilized method_1"""

    def execute(self): ...


class ALSCountClassMethod(PatternClass):
    def class_function(self, arg: dict) -> list:
        if arg:
            ALS_record = list(map(lambda x: x["company"] ,filter(lambda x: x["position"] =='1.1', arg.values())))
            records = list(filter(lambda x: "BC" not in x, filter(lambda x: "EU" not in x, ALS_record)))
            print("[*] Count:" , len(set(list(records))))
            return records
        else: ...


class RosterFilterClass(ABC):
    def __init__(self, uploader: DataUploaderClass) -> None:
        self.uploader = uploader

    @abstractmethod
    def class_function(self, arg: dict, *args, **kwargs):
        """Filtered mon rank"""
        if args:
            try:
                records = list(map(lambda x: (x["company"], x["name"], x["paycode"]) ,filter(lambda x: x["rank"] == args[0], arg.values())))
                return records
            except:
                pass
        else: ...


class LieutenantClassMethod(RosterFilterClass):
    def class_function(self, arg: dict):
        return super().class_function(arg, 'LT')

class BattalionChiefClassMethod(RosterFilterClass):
    def class_function(self, arg: dict):
        return super().class_function(arg, 'BC')

class DivisionChiefClassMethod(RosterFilterClass):
    def class_function(self, arg: dict):
        return super().class_function(arg, 'DC')

      
class OvertimeCallBackMethod(PatternClass):
    def class_function(self, arg: dict) -> list:
        if arg:
            now = Formatters.DatetimeTimeFormatter.local_timestamp()
            record = list(map(lambda x: (x["name"], x["paycode"]) ,filter(lambda x: x["end"] > now, filter(lambda x: x["paycode"] =='OTCB', arg.values()))))
            #records = list(filter(lambda x: "BC" not in x, filter(lambda x: "EU" not in x, record)))
            print("[*] Count:" , len(set(list(record))))
            return record
        else: ...

# Main function and logic of the class

def execute(method:str) -> PatternClass:
    registered_methods = {
        "als": ALSCountClassMethod(XMLFileUploader()),
        "lt": LieutenantClassMethod(XMLFileUploader()),
        "bc": BattalionChiefClassMethod(XMLFileUploader()),
        "dc": DivisionChiefClassMethod(XMLFileUploader()),
        "ot": OvertimeCallBackMethod(XMLFileUploader()),
    }
    choice = registered_methods.get(method, None)
    return choice


def main(method:str, verbose=False) -> None:
    """Main function to handle the Pattern Stratigy (Bridge patter included)"""
    class_pattern = execute(method=method)
    file , data = class_pattern.uploader.file_importer()
    parsed_data = class_pattern.class_function(data)
    complete_time = Formatters.DatetimeTimeFormatter.local_timestamp()
    print(f'[*] {file}')
    print(f"[{complete_time}] Execution completed on file name :: {file}")
    if verbose:
        print(parsed_data)


if __name__ == "__main__":
    choice = input("Method choice ('ALS', 'two')?")
    main(method=choice.lower(), verbose=True)


