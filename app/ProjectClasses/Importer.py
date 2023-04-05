
class XmlImporter:
    def __init__(self,filepath: str, filename: str) -> None:
        self.filepath = filepath
        self.filename = filename
         
    def importer(self): 
        import xml.etree.ElementTree as ET
        tree = ET.parse(f"{self.filepath}{self.filename}")
        root = tree.getroot()
        return root
    
