import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 12345)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print("Server is listening for connections...")

while True:
    # Wait for a connection
    client_socket, client_address = server_socket.accept()

    try:
        print(f"Connection from {client_address}")

        # Receive data from the client
        data = client_socket.recv(1024)
        if data:
            print(f"Received: {data.decode('utf-8')}")

    finally:
        # Clean up the connection
        client_socket.close()
