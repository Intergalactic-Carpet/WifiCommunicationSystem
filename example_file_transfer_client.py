from WifiCommunicationSystem import Client, receive_file
from time import sleep

client = Client(client_name='Client', target_ip=ip, target_port=port)
connected_client = client.connect_and_authenticate('handshake')
if connected_client is not None:
    print(f'Connected to {client.server_name}|{client.server_address[0]}')
    sleep(0.1)
    receive_file(connected_client)
    connected_client.close()
else:
    print("Error: Failed to connect")
