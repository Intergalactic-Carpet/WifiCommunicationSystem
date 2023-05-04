import socket
import os


def receive_file(client_socket):
    """
    Receives incoming files from a server/client

    :param client_socket: The socket of the server/client sending the file
    """
    file_info = client_socket.recv(1024).decode()
    if len(file_info) > 1:
        file_name, file_size = file_info.split(':')
        file_size = int(file_size)
        client_socket.sendall('File Data Received'.encode())
        print(f"Receiving file {file_name} ({file_size} bytes)")

        with open(file_name, 'wb') as f:
            bytes_received = 0
            while bytes_received < file_size:
                buffer = client_socket.recv(min(4096, file_size - bytes_received))
                bytes_received += len(buffer)
                f.write(buffer)
        print(f"File {file_name} received successfully")
    else:
        print('No File Received')


def send_file(client_socket, file_path):
    """
    Sends a file to a server/client

    :param client_socket: The socket of the server/client to send the file to
    :param file_path: The Path of the file you want to send
    """
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    client_socket.sendall(f"{file_name}:{file_size}".encode())
    data = client_socket.recv(1024).decode()
    if data == 'File Data Received':
        with open(file_path, 'rb') as f:
            bytes_sent = 0
            while bytes_sent < file_size:
                buffer = f.read(4096)
                bytes_sent += client_socket.send(buffer)
        print(f"File {file_name} sent successfully")
    else:
        print(f'File could not be sent as the receiver did not signal that it received the data')


def send(client_socket, msg):
    """
    Sends a message to the server/client

    :param client_socket: The socket of the server/client to send the message to

    :param msg: Message to be sent
    """
    client_socket.sendall(str(msg).encode())


def receive(client_socket, buffer_size=1024):
    """
    Receives a message from a server/client

    :param client_socket: The socket of the server/client to receive the message from

    :param buffer_size: Buffer Size
    """
    return client_socket.recv(buffer_size).decode()


class Server:
    def __init__(self, server_name, ip, port):
        """
        Creates a server object with basic authentication for connecting clients.
        !! NOT FOR INDUSTRIAL/COMMERCIAL USE !!

        :param server_name: Name of the server
        :param ip: IP of the server
        :param port: Port of the server
        """
        self.address = (ip, port)
        self.server_name = server_name
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(self.address)
        self.server = server
        print('Server Online')
        print(f'Server Listening on {ip}|{port}')

    def connect_and_authenticate(self, passkey, backlog=1):
        """
        Attempts to connect and authenticate a client

        :param passkey: The correct key for the client to send to the server to complete the handshake
        :param backlog: Backlog
        :return: (client socket, client address, client name) or None if it fails authentication
        """
        print('Server Awaiting Connection...')
        self.server.listen(backlog)
        client_socket, client_address = self.server.accept()
        print('Detected Client')
        print(f'Client Address: {client_address[0]}')
        print('Attempting Handshake...')
        client_socket.sendall('pass?'.encode())
        auth = client_socket.recv(1024).decode()
        if auth == passkey:
            client_socket.sendall('accepted'.encode())
            print('Client Authentication Accepted')
            client_socket.sendall(self.server_name.encode())
            client_name = client_socket.recv(1024).decode()
            return client_socket, client_address, client_name
        else:
            print('Client Authentication Failed')
            client_socket.close()
            return None


class Client:
    def __init__(self, client_name, target_ip, target_port):
        """
        Creates a client object with basic authentication for connecting to servers.
        !! NOT FOR INDUSTRIAL/COMMERCIAL USE !!

        :param client_name: Name of the client
        :param target_ip: IP of the target server
        :param target_port: Port of the target server
        """
        self.name = client_name
        self.server_name = None
        self.server_address = (target_ip, target_port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_and_authenticate(self, passkey):
        """
        Attempts to connect to a server and authenticate itself

        :param passkey: The authentication key to connect to the server

        :return: The server socket or None if it fails authentication
        """
        print('Attempting Connection')
        self.server.connect(self.server_address)
        print('Server Connected')
        print('Attempting Handshake...')
        successful = True
        msg = self.server.recv(1024).decode()
        if msg != 'pass?':
            successful = False
        if successful:
            self.server.sendall(passkey.encode())
            msg = self.server.recv(1024).decode()
            if msg == 'accepted':
                self.server.sendall(self.name.encode())
                self.server_name = self.server.recv(1024).decode()
                return self.server
        print('Client Authentication Failed')
        self.server.close()
        return None
