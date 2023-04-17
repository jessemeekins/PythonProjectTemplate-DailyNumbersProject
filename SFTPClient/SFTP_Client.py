#!/usr/bin/
"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""

import logging
import paramiko
from FileConfig import FileConfig
from abc import ABC, abstractmethod
from datetime import datetime as dt

logging.basicConfig(filename='SFTP_logs.log', level=logging.DEBUG)

now=dt.now()


class SFTPClient(ABC):
    """SFTP Client Methods"""
    def __init__(self, kwargs: dict) -> None:
        self.location = kwargs.get("location", None)
        self.port = kwargs.get("port", None)
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.extension = kwargs.get('extension', None)
        self.filename = kwargs.get('filename', None)
        self.destination = kwargs.get('destination', None)
        self.debug = kwargs.get("debug", True)

    def sftp_client_connect(self) -> object:
        try:
            ssh_client = paramiko.SSHClient()
            logging.info(f"[{now}] SSHClient initialized")
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=self.location, port=self.port, username=self.username, password=self.password, banner_timeout=200)
            ftp_client=ssh_client.open_sftp()
            return ftp_client, ssh_client
        except Exception as e:
            logging.error(f"[*] Connection failed at [{now}]")
            logging.error(f"[*] {e}")

    @abstractmethod
    def file_transfer(self):
        """File transfer"""
     
class SFTPGetClass(SFTPClient):
    def file_transfer(self) -> None:
        """Get Method"""
        ftp_client, ssh = self.sftp_client_connect()
        try:
            # (external Source, internal destination)
            ftp_client.get(f'{self.extension}{self.filename}', f"{self.destination}{self.filename}")
            ftp_client.close()
            logging.info(f'[{now}] :: FILE DOWNLOAD COMPLETE:: {self.filename}')
        except Exception as e:
            logging.error(f"[*] {e}")
            logging.error(f"[{now}] File not downloaded...")
            ftp_client.close()
        ssh.close()
        

class SFTPPutClass(SFTPClient):
    def file_transfer(self) -> None:
        """ Post Method"""
        ftp_client, ssh = self.sftp_client_connect()
        try:
            # ( internal source, external destination)
            ftp_client.put(f'{self.location}{self.filename}', f"{self.destination}{self.filename}")
            ftp_client.close()
            logging.info(f'[{now}] :: FILE TRANSFER COMPLETE :: {self.filename}')
        except Exception as e:
            logging.error(f"[*] {e}")
            logging.error(f"[{now}] File not transferred ...")
            ftp_client.close()
        ssh.close()
        


def SFTP_MAIN(configs, debug=True):
        config = FileConfig(configs).get_file_data()
        if debug:
            print(config)
            print("Test Complete")
        else:
            SFTPGetClass(config).file_transfer()




