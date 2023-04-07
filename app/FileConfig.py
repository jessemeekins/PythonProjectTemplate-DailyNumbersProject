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
import os
from dataclasses import dataclass
from datetime import datetime, timedelta

def adjusted_time():
    today = datetime.today() - timedelta(hours=7)
    formatted_time = datetime.strftime(today, "%Y-%m-%d")
    return formatted_time
    
formatted_time = adjusted_time()

@dataclass
class FileConfig:

    configuration = {
        "PAR" : {"port": os.environ["SFTP_PORT"], 
        "username": os.environ["SFTP_USERNAME"], 
        "password": os.environ["SFTP_PASSWORD"],
        "location": os.environ["IP_ADDRESS"], 
        "extension": os.environ["FILE_EXTENSION"], 
        "destination": os.environ["LOCAL_PATH"], 
        "filename": f'ROS11 MFD{formatted_time}.xml', 
        "debug": True},
    }

    def __init__(self, config: str) -> None:
        self.config = config
            
    def get_file_data(self) -> dict:
        config = self.configuration.get(self.config, '')
        return config

    
FileConfig("PAR")



    
