import socket

# manual edit required
host = ""
port = 45566

try:
    # socket creation
    s = socket.socket()
except Exception as e:
    print(f"Socket creation error: {e}")


def bind_socket():
    try:
        # socket binding with host and port
        s.bind((host, port))
        s.listen(5)
    except Exception as e:
        print(f"Socket binding error: {e}\nRetrying...")
        bind_socket()


def accept_client():
    try:
        # print(f"Connection from {address} is now established!")
        while True:
            # connect with client
            client, address = s.accept()
            cmd = input()
            client.send(str.encode(cmd, "utf-8"))
            if cmd == "quit":
                break
            elif len(cmd) > 0:
                print("here1")
                client_response = client.recv(1024).decode("utf-8")
                print("here2")
                print(client_response, end="")
            print("here3")
            client.close()
        s.close()
    except Exception as e:
        print(f"Client connection error: {e}")


# def send_commands(client):
#     while True:
#         cmd = input()
#         if cmd == "quit":
#             client.send(str.encode(cmd, "utf-8"))
#             break
#         elif len(cmd) > 0:
#             client.send(str.encode(cmd, "utf-8"))
#             client_response = client.recv(1024).decode("utf-8")
#             print(client_response, end="")
#     client.close()
#     s.close()


def main():
    bind_socket()
    accept_client()


main()
