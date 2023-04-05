#%%
from _secrets import Secrets as s
from dataclasses import dataclass

from datetime import datetime, timedelta
today = datetime.today() - timedelta(hours=7)
formatted_time = datetime.strftime(today, "%Y-%m-%d")


class FileConfig:
        
    configuration = {
        
        "DOCKER" : {"port": s.PORT, "username": s.SFTP_USERNAME, "password": s.SFTP_PASSWORD,"location":s.IP_ADDRESS, "extension":s.FILE_EXTENSION, "destination": s.DOCKER_PATH, "filename": f'ROS11 MFD{formatted_time}.xml', "debug": True},
        "DEV" : {"port": s.PORT, "username": s.SFTP_USERNAME, "password": s.SFTP_PASSWORD,"location":s.IP_ADDRESS, "extension":s.FILE_EXTENSION, "destination": s.PROJECT_PATH, "filename": f'ROS11 MFD{formatted_time}.xml', "debug": True},
        "PAR" : {"port": s.PORT, "username": s.SFTP_USERNAME, "password": s.SFTP_PASSWORD,"location":s.IP_ADDRESS, "extension":s.FILE_EXTENSION, "destination": s.LOCAL_PATH, "filename": f'ROS11 MFD{formatted_time}.xml', "debug": True},
        "FULL" : {"port": s.PORT, "username": s.SFTP_USERNAME, "password": s.SFTP_PASSWORD,"location":s.IP_ADDRESS, "extension":s.FILE_EXTENSION, "destination": s.TEST_PATH, "filename": f'ROSTER MFD{formatted_time}.xml', "debug": True},
        
    }
    def __init__(self, config: str) -> None:
        self.config = config
            
    def get_file_data(self) -> dict:
        config = self.configuration.get(self.config, '')
        return config

    


    
