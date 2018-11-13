import socket, select, sys

nick = ''


# Prompt <You>
def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


if __name__ == "__main__":

    host = "localhost"
    port = 14588

    # If no parameter use default host and port
    if (len(sys.argv) == 1):
        print('connect to localhost:14588...\n')

    # One parameter case: host
    if (len(sys.argv) == 2):
        host = sys.argv[1]
        sys.exit()

    # Two parameter case: host and case
    if (len(sys.argv) == 3):
        host = sys.argv[1]
        port = int(sys.argv[2])

    # Build TCP connection via ipv4
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # Connect Process
    try:
        s.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()

    # Loop to check name (name send to server to check in a loop until name is legal)
    while 1:

        # Nickname input
        try:
            nick = input("input your nickname: ")
        except KeyboardInterrupt:
            # Confirm client will broke the connect after Ctrl+C
            s.close()
            sys.exit()

        if nick != "":
            s.send(nick.encode())
            Message = s.recv(4096).decode()
            if Message != "False":
                # Admin account's password required process
                if Message == "PASSWORD":
                    passwd = input('Required Password: ')
                    s.send(passwd.encode())
                    if s.recv(4096).decode() == "Wrong":
                        print("Wrong Passwrod!\n")
                        s.close()
                        sys.exit()
                break
            else:
                print('Name is used, try another one\n')

    print('Connected to remote host. Start sending messages')
    prompt()

    # Loop thread to receive and send message
    while 1:
        rlist = [sys.stdin, s]

        # A-sync I/O
        read_list, write_list, error_list = select.select(rlist, [], [])

        for sock in read_list:
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    # No data mains disconnect
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    sys.stdout.write(data.decode())
                    prompt()

            else:
                msg = sys.stdin.readline()
                s.send(msg.encode())
                prompt()
