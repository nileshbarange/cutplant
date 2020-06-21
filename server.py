import socket

host = ''

port = 5560

storedValue = "Yo Nilesh"

def setupServer():
    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
    try:
        s.bind((host, port))

    except socket.error as msg:
        print(msg)

    print("Socket bind complete")
    return s

def setupConnection():
    s.listen(1) # Allows one coonection as a time
    conn, address = s.accept()
    print("Connected to: " +address[0] + ":" + str(address[1]))
    return conn
def GET():
    reply = storedValue
    return reply

def REPEAT (dataMessage):
    reply = dataMessage [1]
    return reply




def dataTransfer(conn):
    while True:
        data = conn.recv(1024)
        # receive the data
        data = data.decode('utf-8')
        # split the data that you separate the command
        dataMessage = data.split(' ', 1)
        command = dataMessage [0]
        if command == 'GET':
            reply = GET()
        elif command == 'REPEAT':
            reply = REPEAT(dataMessage)
        elif command == 'EXIT':
            print("Our client has left us :(")
            break

        elif command == 'KILL':
            print("Server shutting down")
            break
        else:
            reply = 'Unknown Command'

        # send the replay back to the client

        conn.sendall(str.encode(reply))
        print("data send")
    conn.close()


    #a bid loop that sends/receives data until told not storedValue




s = setupServer()

while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)

    except:
        break
