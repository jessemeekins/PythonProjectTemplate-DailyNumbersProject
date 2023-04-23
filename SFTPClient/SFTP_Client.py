#!/usr/sh/
"""
Copyright (c) 2023 Jesse Meekins
See project 'license' file for more informations
"""
import sys
import logging
import paramiko
from request_config import FileConfig
from abc import ABC
from datetime import datetime as dt


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(logging.FileHandler('SFTP_logs.log'))

now=dt.now()


class SFTPClient(ABC):
    """SFTP Client Methods"""
    def __init__(self, kwargs) -> None:
        ...

    @classmethod
    def connect(cls, **kwargs):
        try:
            ssh_client = paramiko.SSHClient()
            logging.info(f"[{now}] SSHClient initialized")
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=kwargs["location"], port=kwargs["port"], username=kwargs["username"], password=kwargs["password"], banner_timeout=200)
            ftp_client = ssh_client.open_sftp()
            return cls(ftp_client, ssh_client, kwargs)
        except Exception as e:
            logging.error(f"[*] Connection failed at [{now}]")
            logging.error(f"[*] {e}")

    def file_transfer(self):
        """File transfer"""
     
class SFTPGet(SFTPClient):
    def __init__(self, ftp_client, ssh_client, kwargs):
        super().__init__(kwargs)
        self.ftp_client = ftp_client
        self.ssh_client = ssh_client
        self.filename = kwargs['filename']
        self.extension = kwargs["extension"]
        self.destination = kwargs['destination']

    def file_transfer(self) -> None:
        """Get Method"""
        try:
            # (external Source, internal destination)
            self.ftp_client.get(f"{self.extension}{self.filename}", f"{self.destination}{self.filename}")
            self.ftp_client.close()
            logging.info(f"[{now}] :: FILE DOWNLOAD COMPLETE:: {self.filename}")
        except Exception as e:
            logging.error(f"[*] {e}")
            logging.error(f"[{now}] File not downloaded...")
            self.ftp_client.close()
        self.ssh_client.close()
        

class SFTPPut(SFTPClient):
    def __init__(self, ftp_client, ssh_client, kwargs):
        super().__init__(kwargs)
        self.ftp_client = ftp_client
        self.ssh_client = ssh_client
        self.filename = kwargs['filename']
        self.extension = kwargs["extension"]
        self.destination = kwargs['destination']

    def file_transfer(self) -> None:
        """Post Method"""
        try:
            # Open local file and upload it to SFTP server
            with open(self.filename, "rb") as f:
                self.ftp_client.put(f, f"{self.destination}{self.filename}")
            logging.info(f"[{now}] :: FILE TRANSFER COMPLETE :: {self.filename}")
        except Exception as e:
            logging.error(f"[*] {e}")
            logging.error(f"[{now}] File not transferred ...")
        finally:
            self.ftp_client.close()
            self.ssh_client.close()

        


def sftp_main(config_name):
    config = FileConfig(config_name).get_file_data()
    if config["transfer_type"] == "get":
        sftp_client = SFTPGet.connect(**config)
    elif config["transfer_type"] == "put":
        sftp_client = SFTPPut.connect(**config)
    else:
        logging.error(f"[{now}] Unknown transfer type: {config['transfer_type']}")
        return

    try:
        sftp_client.file_transfer()
    except Exception as e:
        logging.error(f"[*] {e}")
    finally:
        del sftp_client





