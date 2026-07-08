import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

username = input("Enter your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()

            if message == "USERNAME":
                client.send(username.encode())
            else:
                print(message)

        except:
            print("Disconnected from server.")
            client.close()
            break


def send_messages():
    while True:
        try:
            text = input()

            if text.strip() == "":
                continue

            message = f"{username}: {text}"

            client.send(message.encode())

        except:
            client.close()
            break


receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()