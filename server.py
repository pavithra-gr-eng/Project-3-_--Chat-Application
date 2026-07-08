import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []


def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                remove_client(client)


def remove_client(client):
    if client in clients:
        index = clients.index(client)

        username = usernames[index]

        clients.remove(client)
        usernames.remove(username)

        client.close()

        print(f"{username} disconnected.")

        broadcast(f"{username} left the chat.".encode())


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)

            if not message:
                raise Exception()

            decoded = message.decode()

            print(decoded)

            broadcast(message, client)

        except:
            remove_client(client)
            break


def receive_connections():
    print(f"Server started on {HOST}:{PORT}")
    print("Waiting for clients...\n")

    while True:

        client, address = server.accept()

        print(f"Connected: {address}")

        client.send("USERNAME".encode())

        username = client.recv(1024).decode()

        usernames.append(username)
        clients.append(client)

        print(f"{username} joined the chat.")

        broadcast(f"{username} joined the chat.".encode())

        client.send("Connected successfully.".encode())

        thread = threading.Thread(
            target=handle_client,
            args=(client,)
        )

        thread.start()


receive_connections()