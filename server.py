import socket, select, re

# Three list to storage socks, nicknames and their status
CONNECTION_LIST = []
NICK_NAME = []
STATUS_LOG = []


# Broadcast Function
def broadcast_data(sock, message):
    print(message)
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:  # Do not send message to server and self
            try:
                index = CONNECTION_LIST.index(sock)
                socket.send(message.encode())
                STATUS_LOG[index] = STATUS_LOG[index] + str(message)
            except:
                socket.close()
                CONNECTION_LIST.remove(socket)


# The Process to disconnect a User
def user_disconnect(sock, addr, nick):
    broadcast_data(sock, "User (%s) is offline\n" % nick)
    if addr != '':
        print("Client (%s, %s) is offline" % addr)
    sock.close()
    # Remove from the list
    STATUS_LOG.pop(CONNECTION_LIST.index(sock))
    NICK_NAME.remove(nick)
    CONNECTION_LIST.remove(sock)


# The method of LIST command
def list_user(sock):
    data = "\n[LIST]--------------------------\n" + "There are " + str(
        len(NICK_NAME)) + " users in the chatroom, they are:\n"
    for i in NICK_NAME:
        data = data + str(i) + "\n"
    data = data + "--------------------------------\n"
    sock.send(data.encode())
    index = CONNECTION_LIST.index(sock)
    STATUS_LOG[index] = STATUS_LOG[index] + str(data)


# The method to check is the new nickname have been used and is legal
def checkName(name):
    if not re.match('^[\u4e00-\u9fa5a-zA-Z]+$', str(name)):  # Chinese or Alphabet allowed
        return False
    for i in NICK_NAME:
        if str(name) == str(i):
            return False
    return True


# The method to kick user
def kickhe(name):
    index = NICK_NAME.index(name)
    if name.encode().decode() in NICK_NAME:
        print("find it")
        user_disconnect(CONNECTION_LIST[index], '', NICK_NAME[index])
    else:
        print("????")


# The method of show status
def showStatus(name, sock):
    sock.send(("\n[STATUS]------------------------\n" + STATUS_LOG[
        NICK_NAME.index(name)] + "--------------------------------\n").encode())
    STATUS_LOG[CONNECTION_LIST.index(sock)] += "Use Status Command see " + str(name) + "'s status\n"


if __name__ == "__main__":

    RECV_BUFFER = 4096
    PORT = 14588

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp via ipv4
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allowed (PAT?) addresses
    server_socket.bind(("0.0.0.0", PORT))  # Bind the address and port
    server_socket.listen(10)  # max number of connection is 10

    # Add server to three list
    CONNECTION_LIST.append(server_socket)
    NICK_NAME.append("server")
    STATUS_LOG.append('')

    print("Chat server started on port " + str(PORT))

    # Big endless while loop thread
    while 1:
        # Asynchronous I/O to control mult-socket at same time
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
            if sock in read_sockets:
                nick = NICK_NAME[CONNECTION_LIST.index(sock)]
                if sock == server_socket:
                    # The Server-socket
                    sockid, addr = server_socket.accept()
                    while 1:
                        nick = sockid.recv(RECV_BUFFER).decode()
                        try:
                            if nick == "Admin":  # If is administration accout, require password
                                PP = 'PASSWORD'
                                sockid.send(PP.encode())
                                if sockid.recv(RECV_BUFFER).decode() != "123":
                                    WW = "Wrong"
                                    sockid.send(WW.encode())
                                    break

                            # Check Name is legal
                            if checkName(nick):
                                TT = 'Ture'
                                sockid.send(TT.encode())
                                # Append information to list
                                CONNECTION_LIST.append(sockid)
                                NICK_NAME.append(nick)
                                STATUS_LOG.append('')
                                print("Client (%s, %s) connected" % addr)
                                broadcast_data(sockid, "[%s] entered room, Welcome!\n" % nick)
                                break
                            else:
                                FF = 'False'
                                sockid.send(FF.encode())
                        except:
                            # Avoid Server crash because of broken pipe
                            break

                # The client socket
                else:
                    try:
                        index = CONNECTION_LIST.index(sock)
                        data = sock.recv(RECV_BUFFER).decode()
                        # To listen is the command have be used by the user
                        if str(data) == "\n":  # To avoid void message to be boardcast
                            continue
                        elif str(data) == "/exit\n":  # Exit command listener
                            user_disconnect(sock, addr, nick)
                            continue
                        elif str(data) == "/list\n":  # List command listener
                            list_user(sock)
                            continue
                        elif (str(data).split())[0] == "/status":  # Status command listener
                            showStatus((str(data)).split()[1], sock)
                            continue
                        elif (str(data).split())[0] == "/kick":  # Kick command Listener
                            if nick == "Admin":  # Check if he is an admin
                                BadGuy = (str(data).split())[1]
                                sock.send(("You kick " + BadGuy + "\n").encode())
                                STATUS_LOG[index] = STATUS_LOG[index] + "You kick " + BadGuy + "\n"
                                try:
                                    kickhe(BadGuy)
                                except:
                                    print("Error")
                                    continue
                            else:
                                # No premission error
                                sock.send("You have no premission to use KICK command\n".encode())
                                STATUS_LOG[index] = STATUS_LOG[index] + "You have no premission to use KICK command\n"
                            continue
                        else:
                            if data:
                                broadcast_data(sock, "\r" + '<' + str(nick) + '>: ' + data)
                    except:
                        user_disconnect(sock, addr, nick)
                        continue

    server_socket.close()
