import sys, socket, select

if(len(sys.argv) == 3):
    ipaddr = sys.argv[1]
    try:
        socket.inet_aton(ipaddr)
    except socket.error:
        print("IP address is invalid. Please try again.")
        sys.exit()

    argportnumber = sys.argv[2]

else:
    print("Too little or too many arguments")
    sys.exit()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print("socket creation failed")

try:
    print("Trying to connect to chat server...")
    s.connect((""+ipaddr, int(argportnumber)))
    serverwelcome = s.recv(2048).decode()
    sys.stdout.write(serverwelcome)

except:
    print("Connection failed. Chat server maybe busy/full/down or IP address/port number may be wrong. Please try again.")
    sys.exit()

while True:
    #two ways of input here: either user wants to broadcast a message from sys.stdin or server is sending a message to the user
    twoinput = [sys.stdin, s]
    read_sockets, write_socket, error_socket = select.select(twoinput,[],[])

    for socket in read_sockets:
        #we have a message from the server
        if(socket == s):
            message = socket.recv(2048)
            if not message:
                print("\r\n" + "\r\n" + "Server closed the connection. Goodbye!")
                sys.exit()
            else:
                print("\r\n")
                print(message.decode())
                print()
                sys.stdout.write("You> ")
                sys.stdout.flush()

        #user has sent a message
        else:
            print()
            usermessage = input("You> ")
            checkforexit = usermessage.upper()
            if(checkforexit == "EXIT"):
                s.close()
                print("\r\n" + "\r\n" + "You have disconnected from the server.")
                sys.exit()

            s.send(usermessage.encode())
            sys.stdout.flush()
