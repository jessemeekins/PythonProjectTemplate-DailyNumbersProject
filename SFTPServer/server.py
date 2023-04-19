
import os
import paramiko

# Define the SFTP server parameters
HOST = '0.0.0.0'
PORT = 22
USERNAME = 'myuser'
PASSWORD = 'mypassword'

# Define the server's root directory
ROOT_DIR = '/home/myuser/sftp'

# Define the SFTP server class
class SFTPServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = None
    def check_auth_password(self, username, password):
        if username == USERNAME and password == PASSWORD:
            return paramiko.AUTH_SUCCESSFUL
        else:
            return paramiko.AUTH_FAILED
    def check_channel_request(self, kind, channel_id):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        else:
            return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

# Create the SFTP server
server = paramiko.Transport((HOST, PORT))
server.add_server_key(paramiko.RSAKey.generate(2048))
server.start_server(server=SFTPServer())

# Set up the server's root directory
if not os.path.exists(ROOT_DIR):
    os.mkdir(ROOT_DIR)

# Serve the SFTP client connections
while True:
    client, addr = server.accept()
    print(f"Connected to {addr}")
    try:
        client.auth_none(username='')
        sftp = paramiko.SFTPClient.from_transport(client)
        sftp.chdir(ROOT_DIR)
        print(f"Serving SFTP client {addr}")
        while True:
            command = sftp.get_command()
            if command is None:
                break
            if command[0] == 'get':
                sftp.get(command[1], command[2])
            elif command[0] == 'put':
                sftp.put(command[1], command[2])
        sftp.close()
    except paramiko.SSHException:
        print(f"Failed to serve SFTP client {addr}")
        client.close()
