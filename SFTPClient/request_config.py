#%%
"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""
from pathlib import Path
from  _secrets import Secrets as s
from datetime import datetime, timedelta

# Import secrets directly
SFTP_USERNAME = s.SFTP_USERNAME
SFTP_PASSWORD = s.SFTP_PASSWORD
IP_ADDRESS = s.IP_ADDRESS
PORT = s.PORT
EXPORT_FILE_EXTENSION = s.EXPORT_FILE_EXTENSION
SERVER_PATH = s.SERVER_PATH
PROJECT_PATH = s.PROJECT_PATH
GET = "get"

formatted_time = datetime.strftime(datetime.today() - timedelta(hours=7), "%Y-%m-%d")

class FileConfig:
        
    configuration = {
        "DEV_PAR": {
            "transfer_type": GET,
            "port": PORT,
            "username": SFTP_USERNAME,
            "password": SFTP_PASSWORD,
            "location": IP_ADDRESS,
            "extension": EXPORT_FILE_EXTENSION,
            "destination": PROJECT_PATH,
            "filename": f"ROS11 MFD{formatted_time}.xml",
            "debug": True,
        },
        "DEV_FULL": {
            "transfer_type": GET,
            "port": PORT,
            "username": SFTP_USERNAME,
            "password": SFTP_PASSWORD,
            "location": IP_ADDRESS,
            "extension": EXPORT_FILE_EXTENSION,
            "destination": PROJECT_PATH,
            "debug": True,
            "filename": f'Full Roster Export Hourly{formatted_time}_{formatted_time}.xml'
        },
        "PROD_FULL": {
            "transfer_type": GET,
            "port": PORT,
            "username": SFTP_USERNAME,
            "password": SFTP_PASSWORD,
            "location": IP_ADDRESS,
            "extension": EXPORT_FILE_EXTENSION,
            "destination": SERVER_PATH,
            "debug": True,
            "filename": f'Full Roster Export Hourly{formatted_time}_{formatted_time}.xml'
        },
        "PROD_PAR": {
            "transfer_type": GET,
            "port": PORT,
            "username": SFTP_USERNAME,
            "password": SFTP_PASSWORD,
            "location": IP_ADDRESS,
            "extension": EXPORT_FILE_EXTENSION,
            "destination": SERVER_PATH,
            "filename": f"ROS11 MFD{formatted_time}.xml",
            "debug": True,
        },
    }
    
    def __init__(self, config: str) -> None:
        self.config = config.upper()
            
    def get_file_data(self) -> dict:
        config = self.configuration.get(self.config, {})
        formatted_time = datetime.strftime(datetime.today() - timedelta(hours=7), "%Y-%m-%d")
        config["filename"] = config.get("filename", "").format(formatted_time=formatted_time)

        Path(config["destination"]).mkdir(parents=True, exist_ok=True)

        return config

