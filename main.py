from sender import *

if __name__ == "__main__":
    sender = Sender()
    for i in range(1,10):
        sender.rdt_send("msg" + str(i))