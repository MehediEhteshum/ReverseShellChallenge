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
        # connect with client
        client, address = s.accept()
        print(f"Connection from {address} is now established!")
        # send commands to client and process client response
        send_commands(client)
        client.close()
        s.close()
    except Exception as e:
        print(f"Client connection error: {e}")


def send_commands(client):
    # send commands to client and process client response
    while True:
        cmd = input()  # give your input command
        if cmd == "quit":
            # exits the program on both sides
            # send command to client (no empty commands)
            client.send(str.encode(cmd, "utf-8"))
            break
        elif len(cmd) > 0:
            # send command to client (no empty commands)
            client.send(str.encode(cmd, "utf-8"))
            # receives client response
            client_response = client.recv(8).decode("utf-8")
            while len(client_response) > 0:
                # receives and accumulataes client full response
                client.settimeout(0.5)
                try:
                    # receives part of response
                    res_part = client.recv(8).decode("utf-8")
                except Exception as e:
                    res_part = ""
                if len(res_part) <= 0:
                    break
                client_response += res_part  # accumulates response
            print(client_response, end="")


def main():
    bind_socket()
    accept_client()


main()
