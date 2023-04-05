__author__ = 'Jesse Meekins'

import socket
import threading

HOST, PORT = '192.168.1.255', 6000

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen(10)

    while True:
        client, address = server_socket.accept()
        print(f"[*] Accepting connection from {address[0]}:{address[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f"[*] Recieved: {request.decode('utf-8')}")
        sock.send('ACK')

if __name__ == "__main__":
    main()
