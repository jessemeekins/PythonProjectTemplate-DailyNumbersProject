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

from mapper import DataFieldsMapper

class DataParser:
    """Loops though each record of records in a XML file, 'key_tag' set to record,
    the internal file tag for each individual record in telestaff in a given report"""
    def __init__(self, data, mapper: DataFieldsMapper, key_tag='Record') -> None:
        self.data = data
        self.mapper: DataFieldsMapper = mapper
        self.key = key_tag


    def xml_into_dictionary(self) -> dict:
        """Takes in the XML.Tree from the XMLImporter Class and loops through the records"""
        records_dict = dict()
        for i, child in enumerate(self.data.iter(self.key)):
            record = self.mapper.field_mapper(child)
            records_dict[i] = record
        return records_dict

