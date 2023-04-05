#%%

from SFTPClient._secrets import Secrets
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
        "PAR" : {"port": Secrets.PORT, 
        "username": Secrets.SFTP_USERNAME, 
        "password": Secrets.SFTP_PASSWORD,
        "location":Secrets.IP_ADDRESS, 
        "extension":Secrets.FILE_EXTENSION, 
        "destination": Secrets.LOCAL_PATH, 
        "filename": f'ROS11 MFD{formatted_time}.xml', 
        "debug": True},
    }

    def __init__(self, config: str) -> None:
        self.config = config
            
    def get_file_data(self) -> dict:
        config = self.configuration.get(self.config, '')
        return config

    
FileConfig("PAR")



    
