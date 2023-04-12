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
#%%
import xml.etree.ElementTree as ET
from filepaths import FILE_PATH_FACTORY

class XmlImporter:
    """Initialized with filepath: str and filename: str"""
    def __init__(self,filepath: str, filename: str) -> None:
        self.filepath = filepath
        self.filename = filename
      
    def importer(self): 
        """Located the file to parse and return xml.etree.ElementTree obj"""
        tree = ET.parse(f"{self.filepath}{self.filename}")
        root = tree.getroot()
        return root
    
f = FILE_PATH_FACTORY["ALS"]
f.filepath, f.filename