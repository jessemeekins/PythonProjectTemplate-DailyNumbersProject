import socket

target = '192.168.1.255'
port = 6000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target,port))
client.send(b'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n')

response = client.recv(4096)
print(response.decode())
client.close()