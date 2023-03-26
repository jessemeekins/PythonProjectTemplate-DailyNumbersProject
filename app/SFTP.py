import logging
import paramiko
from datetime import datetime as dt

logging.basicConfig(filename='//SFTP_logs.log', filemode='w', level=logging.DEBUG)
now=dt.now()

class SFTPClient:
    """SFTP Client Methods"""
    def __init__(self, IP_ADDRESS, PORT, USERNAME, PASSWORD, FILE_EXTENSION, FILENAME, LOCAL_PATH) -> None:
        self.ip = IP_ADDRESS
        self.port = PORT
        self.username = USERNAME
        self.password = PASSWORD
        self.ext = FILE_EXTENSION
        self.file = FILENAME
        self.localpath = LOCAL_PATH
        
    def get_file_client(self) -> None:
        """Get Method"""
        try:
            ssh_client = paramiko.SSHClient()
            logging.info(f"[{now}] SSHClient initialized")
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh_client.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password)
            logging.info(f"[{now}] SSHClient connected")
            ftp_client=ssh_client.open_sftp()
            logging.info(f"[{now}] SFTP connected")
            ftp_client.get(f'{self.ext}{self.file}', self.localpath)
            logging.info(f"[{now}] Located :: {self.ext}{self.file} :: Sending to :: {self.localpath} ::")
            logging.info(f'[{now}] :: File Downloaded ::')
            ftp_client.close()
            logging.info(f'[{now}] :: FILE :: {self.file} :: Complete ::')
        except Exception as e:
            logging.error(f"[*] {e}")

    def post_file_client(self) -> None:
        """ Post Method"""


