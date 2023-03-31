#%%

from app.secrets import *
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
        "PAR" : {"port": PORT, 
        "username": SFTP_USERNAME, 
        "password": SFTP_PASSWORD,
        "location":IP_ADDRESS, 
        "extension":FILE_EXTENSION, 
        "destination": LOCAL_PATH, 
        "filename": f'ROS11 MFD{formatted_time}.xml', 
        "debug": True},
    }

    def __init__(self, config: str) -> None:
        self.config = config
            
    def get_file_data(self) -> dict:
        config = self.configuration.get(self.config, '')
        return config

    
FileConfig("PAR")



    
