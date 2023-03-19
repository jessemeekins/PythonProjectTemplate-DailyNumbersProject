#%%
import logging
from abc import ABC, abstractmethod
from data.FileTypeFormatter import formaters

log = logging.Logger('default_logger.log')

class DataUploaderClass(ABC):
    @abstractmethod
    def file_importer(self):
        """retrieve file based on file type"""

    @abstractmethod
    def load_data(self):
        """upload file into program ready for logic"""


class XMLFileUploader(DataUploaderClass):
    def file_importer(self) -> str:
        file_name = formaters.XML_importer() 
        print(f"[*] {file_name}")
        return file_name
        
    def load_data(self, filepath: str) -> dict:
        pass

class XLSXFileUploader(DataUploaderClass):
    def file_importer(self) -> str:
        file_name = formaters.XLSX_importer()
        print(f"[*] {file_name}")
        return super().file_importer()
    
    def load_data(self):
        return super().load_data()

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
    def function_1(self) -> None:
        print("[*] PatternClassMethod_1::function_1 executed")

    def function_2(self) -> None:
        print("[*] PatternClassMethod_1::function_2 executed")


class PatternClassMethod_2(PatternClass):
    def function_1(self) -> None:
        print("[*] PatternClassMethod_2::function_1 executed")
        
    def function_2(self) -> None:
        print("[*] PatternClassMethod_2::function_2 executed")


def execute(method:str) -> PatternClass:
    registered_methods = {
        "one": PatternClassMethod_1(XMLFileUploader()),
        "two": PatternClassMethod_2(XLSXFileUploader())
    }
    choice = registered_methods.get(method, None)
    return choice


def main(method:str) -> None:
    class_pattern = execute(method=method)
    class_pattern.uploader.file_importer()
    class_pattern.uploader.load_data()
    class_pattern.function_1()
    class_pattern.function_2()
    print("[*] Execution Complete")

if __name__ == "__main__":
    choice = input("Method choice ('one', 'two')?")
    main(method=choice)

