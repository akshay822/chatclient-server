import sys, socket, select

if(len(sys.argv) == 2):
    argportnumber = sys.argv[1]
else:
    print("Too little or too many arguments.")
    sys.exit()

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server_socket.bind(("", int(argportnumber)))
except:
    print("Argument is not a port number or port number is busy. Please try again.")
    sys.exit()

server_socket.listen(10)

print("Chat server listening on port " + argportnumber + ".\r\n")

#start of the connections list with the server socket
connections = [server_socket]

def broadcast(message, socket):
    for s in connections:
        #send the message to all other clients, excluding server and myself
        if(s != server_socket and s != socket):
            try:
                s.send(message.encode())
            #connection is broken if the send doesn't work
            except:
                s.close()
                connections.remove(s)

while True:
    read_sockets, write_socket, error_socket = select.select(connections,[],[])

    for socket in read_sockets:
        # we've got a connection from a client
        if(socket == server_socket):
            # Establish connection with client.
            c, addr = server_socket.accept()
            connections.append(c)

            sys.stdout.write(str(c.getsockname()) + " has connected.\r\n" + "\r\n")

            # send a welcome message to the client.
            if(len(connections)-1 == 1):
                print("There is currently 1 person in the chat.\r\n")

                c.send("Welcome to the chat server!\r\nThere is currently 1 person in the chat.\r\nYou> ".encode())
            else:
                print("There are currently " + str(len(connections)-1) + " people in the chat.\r\n")

                welcomestring = "Welcome to the chat server!\r\nThere are currently " + str(len(connections)-1) + " people in the chat.\r\nYou> "
                c.send(welcomestring.encode())

            broadcast("(" + str(c.getsockname()[0])+ ")" + " has joined the chat.", c)

        # we've got a message from a client
        else:
            try:
                message = socket.recv(2048).decode()
                if not message:
                    connections.remove(socket)
                    if(len(connections)-1 == 1):
                        print("(" + str(socket.getsockname()[0])+ ")" + "> " + "has left the chat.\r\n\r\nThere is currently 1 person in the chat.\r\n")

                        broadcast("(" + str(socket.getsockname()[0])+ ")" + "> " + "has left the chat.\r\nThere is currently 1 person in the chat.", socket)
                    else:
                        print("(" + str(socket.getsockname()[0])+ ")" + "> " + "has left the chat.\r\n\r\nThere are currently "
                        + str(len(connections)-1) + " people left in the chat.\r\n")

                        broadcast("(" + str(socket.getsockname()[0])+ ")" + "> " + "has left the chat.\r\nThere are currently "
                        + str(len(connections)-1) + " people left in the chat.", socket)
                    socket.close()
                else:
                    print("(" + str(socket.getsockname()[0]) + ")" + "> " + message + "\r\n")
                    broadcast("(" + str(socket.getsockname()[0])+ ")" + "> " + message, socket)
            except:
                socket.close()
                connections.remove(socket)

server_socket.close()
