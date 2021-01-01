from socket import  AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 5500
BUFSIZ = 512
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10


# GLOBAL VARIABLES
persons=[]
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def broadcast(msg, name):
    """
    send new messages to all clients
    @param client:name [bytes]
    """
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8")+msg)
        except Exception as e:
            print("[Exception] @broadcast: ", e)
            break

def client_communication(person):
    """
    Thread to handle all messages from client
    @param client:Person
    @return: None
    """

    client = person.client

    # get person name as first message
    name = client.recv(BUFSIZ).decode("utf8")
    msg = bytes(f"{name} has joined the chat!","utf8")
    broadcast(msg,"") # broadcast welcome message

    while True: # wait for any message from person
        try:
            msg = client.recv(BUFSIZ)
            
            if msg == bytes("{quit}","utf8"):
                broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
                print(f"[DISCONNECTED] {name} disconnected...")
                client.close()
                persons.remove(person)                
                break 
            else:
                broadcast(msg, name+": ")
                print(f"{name}: ", msg.decode("utf8"))

        except Exception as e:
            print("[Exception] @client_communication", e)
            break


def wait_for_connection():
    """
    Wait for connection from new clients, start new thread once connected
    @param SERVER: SOCKET
    @return: None
    """
    
    while True: # wait for any new connections
        try:
            client, addr = SERVER.accept()
            person = Person(addr,client) # create new Person for new connection
            persons.append(person)
            print(f"[CONNECTION]{addr} connected to the server at {time.time()}")
            Thread(target=client_communication,args=(person,)).start()
        except Exception as e:
            print("[FAILURE] @wait_for_connection", e)
            SERVER.close()
            break
    print("SERVER CRASHED")

if __name__ == "__main__":
    SERVER.listen(5)
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
    