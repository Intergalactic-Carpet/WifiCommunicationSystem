from WifiCommunicationSystem import Client

client = Client(client_name='Client', target_ip=ip, target_port=port)
connected_client = client.connect_and_authenticate(passkey='handshake')
if connected_client is not None:
    print(f'Connected to {client.server_name}|{client.server_address[0]}')
    connected_client.close()
else:
    print("Error: Failed to connect")
