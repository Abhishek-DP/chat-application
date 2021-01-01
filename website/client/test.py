import time
from client import Client
from threading import Thread

c1 = Client("Abhishek")
c2 = Client("Shiva Prakash")

def update_messages():
    """
    updates the local list of messages
    @return: None
    """
    msgs = []
    while True:
        time.sleep(0.1) # update every 1/10th of a second
        new_messages = c1.get_messages() # get any new messages from client
        msgs.extend(new_messages) # add to local list of messages

        for msg in new_messages: # display new messages
            print(msg)

            if msg == "{quit}":
                break

Thread(target=update_messages).start()

c1.send_messages("hello")
time.sleep(2)
c2.send_messages("hello")
time.sleep(3)
c1.send_messages("Whats up")
time.sleep(5)
c2.send_messages("Nothing much")
time.sleep(3)
c1.disconnect()
time.sleep(2)
c2.disconnect()
time.sleep(1)