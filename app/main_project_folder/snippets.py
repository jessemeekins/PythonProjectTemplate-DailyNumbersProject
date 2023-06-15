#%%

import xml.etree.ElementTree as ET
import json
from mapper import XmlAlsFieldsMap
def importer():
    """Locate the file to parse and return xml.etree.ElementTree obj"""
    tree = ET.parse(str('/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/exports/ROS11 MFD2023-06-12.xml'))
    root = tree.getroot()
    return root


def _parser_format(data) -> dict:
    """Takes in the XML.Tree from the XMLImporter Class and loops through the records"""
    records_dict = dict()
    for i, child in enumerate(data.iter("Record")):
        record = XmlAlsFieldsMap.field_mapper(child)
        records_dict[i] = record
        print(record)


    return records_dict

def get_positions(data):
    
    positions = dict()
    for record in data.values():
        company = record["PUnitAbrvCh"]
        position = record["PUnitAbrvCh"]

        if company not in positions.keys():
            positions[company] = []
        positions[company] = position

    print(positions)

data = importer()
data = _parser_format(data)

data