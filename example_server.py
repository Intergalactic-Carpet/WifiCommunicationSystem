from WifiCommunicationSystem import Server

server = Server(server_name='Server', ip=ip, port=port)
connection = server.connect_and_authenticate(passkey='handshake')
if connection is not None:
    c_socket, c_address, c_name = connection
    print(f'Connected to {c_name}|{c_address[0]}')
    c_socket.close()
else:
    print("Error: Failed to connect")

server.server.close()
