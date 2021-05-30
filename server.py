from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from time import sleep

#All commands available to use
def commands(client):
    sleep(0.01)
    command = ">> Commands:"
    client.send(bytes(command, "utf8"))
    command = "* !quit - To quit application"
    client.send(bytes(command, "utf8"))
    sleep(0.01)
    command = "* !discon - To disconnect from the chatroom"
    client.send(bytes(command, "utf8"))
    command = "* !help - To view all the commands"
    client.send(bytes(command, "utf8"))

    
#To close a connection
def close_connection(client, name, address, clients):
    print("%s:%s has disconnected." % address)
    client.close()
    del clients[client]
    if (name != ""):
        broadcast(bytes("%s has left the chat." % name, "utf8"))
                
#To accept the connection requests
def accept_incoming_connections():
   
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes(">> Welcome to the chatroom!", "utf8"))
        client.send(bytes(">> Type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

#To send the message to all the present connections
def broadcast(msg, prefix=""): 

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

#To handle the incoming messages appropriately
def handle_client(client):

    try:
        #for new connections
        clients[client] = ""
        name = ""
        name = client.recv(BUFSIZ).decode("utf8")
        print(name," <= ",addresses[client])
    
        welcome = '>> Welcome %s!' % name
        client.send(bytes(welcome, "utf8"))
    
        commands(client)
    
        msg = "%s has joined the chat!" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name

        #incoming messages handling

        while True:
            msg = client.recv(BUFSIZ)
            dis = (bytes("!quit", "utf8"),bytes("!discon", "utf8"))

            #handling disconnect request
            if msg in dis:
                client.send(msg)
                #print(clients)
                close_connection(client, name, addresses[client], clients)
                #print(clients)
                break
            
            #to show present commands
            elif msg == bytes("!help","utf8"):
                commands(client)

            #broadcasting messages
            else:
                broadcast(msg, name+": ")

    #handling connection errors
    except Exception as e:
        close_connection(client, name, addresses[client], clients)
        '''if name != "":
            close_connection(client, name, addresses[client], clients)
        else:
            print("%s:%s has disconnected." % addresses[client])'''
        print("Connection ERROR")

#global variables
clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


#Main for accepting multiple connections
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
