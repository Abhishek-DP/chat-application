from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread,Lock
import time

class Client:
    """
    for communication with server
    """
    HOST = "localhost"
    PORT = 5500
    ADDR = (HOST, PORT)
    BUFSIZ = 512

    def __init__(self, name):
        """
        Init contains all the functions need to work concurrently at start
        @param name:str
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages=[]
        self.lock = Lock()
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_messages(name)

    def receive_messages(self):
        """
        receive messages from server
        @param msg:str
        @return:None
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode()
                # Make sure memory is safe to access
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()                
            except Exception as e:
                print("[Exception]",e)
                break

    def send_messages(self, msg):
        """
        send messages to server
        @param msg:str
        @return: None
        """
        try:
            self.client_socket.send(bytes(msg,"utf8"))
            
            if msg == "{quit}":
                self.client_socket.close()
        except Exception as e:
            # self.client_socket = socket(AF_INET, SOCK_STREAM)
            # self.client_socket.connect(self.ADDR)
            print("[Exception]: ",e)
    
    def get_messages(self):
        """
        returns the list of messages
        @return: list[str]
        """
        messages_copy = self.messages[:]
        # Make sure memory is safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return messages_copy

    def disconnect(self):
        """
        Disconnects from the server
        """
        self.send_messages("{quit}")