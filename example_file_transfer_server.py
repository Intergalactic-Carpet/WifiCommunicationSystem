from WifiCommunicationSystem import Server, send_file
from time import sleep

server = Server(server_name='Server', ip=ip, port=port)
connection = server.connect_and_authenticate('handshake')
if connection is not None:
    c_socket, c_address, c_name = connection
    print(f'Connected to {c_name}|{c_address[0]}')
    sleep(0.1)
    send_file(c_socket, path)
    c_socket.close()
else:
    print("Error: Failed to connect")

server.server.close()
