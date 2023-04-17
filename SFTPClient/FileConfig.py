#%%
"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""

from  _secrets import Secrets as s

from datetime import datetime, timedelta
today = datetime.today() - timedelta(hours=7)
formatted_time = datetime.strftime(today, "%Y-%m-%d")


class FileConfig:
        
    configuration = {
        
        "DOCKER" : {"username": s.SFTP_USERNAME, "password": s.SFTP_PASSWORD,"location":s.IP_ADDRESS, "port": s.PORT, "extension":s.EXPORT_FILE_EXTENSION, "destination": s.DOCKER_PATH, "filename": f'ROS11 MFD{formatted_time}.xml', "debug": True},
        "DEV" : {"port": s.PORT, "username": s.SFTP_USERNAME, "password": s.SFTP_PASSWORD,"location":s.IP_ADDRESS, "extension":s.EXPORT_FILE_EXTENSION, "destination": s.PROJECT_PATH, "filename": f'ROS11 MFD{formatted_time}.xml', "debug": True},
        "BDE_P" : {"port": s.PORT, "username": s.SFTP_USERNAME, "password": s.SFTP_PASSWORD,"location":s.IP_ADDRESS, "extension":s.BDE_FILE_EXTENSION, "destination": s.PROJECT_PATH, "filename": f'BDE_Personnel.xml', "debug": True},
        "TBDE_P" : {"port": s.PORT, "username": s.SFTP_USERNAME, "password": s.SFTP_PASSWORD,"location":s.IP_ADDRESS, "extension":s.BDE_FILE_EXTENSION, "destination": s.PROJECT_PATH, "filename": f'2023-04-06_2023-04-06.xml', "debug": True},
        "FULL" : {"port": s.PORT, "username": s.SFTP_USERNAME, "password": s.SFTP_PASSWORD,"location":s.IP_ADDRESS, "extension":s.EXPORT_FILE_EXTENSION, "destination": s.PROJECT_PATH, "filename": 'Full Roster Export Hourly.xml', "debug": True},
        "CUSTOM" : {"port": s.PORT, "username": s.SFTP_USERNAME, "password": s.SFTP_PASSWORD,"location":s.IP_ADDRESS, "extension":s.EXPORT_FILE_EXTENSION, "destination": s.PROJECT_PATH, "filename": 'ROS11 MFD2023-04-07.xml', "debug": True},
        
    }
    def __init__(self, config: str) -> None:
        self.config = config.upper()
            
    def get_file_data(self) -> dict:

        config = self.configuration.get(self.config, '')
        return config

