from socket import *
from time import sleep
from util import *
## No other imports allowed

'''Directions to run: Please start up receiver.py first. Then main.py. '''

class Receiver:
    def __init__(self, receiver_port):
        self.receiver_port = receiver_port     # receiver port number
        self.receiver_socket = socket(AF_INET, SOCK_DGRAM)
        self.receiver_socket.bind(('', receiver_port)) 
        self.expected_seq_num = 0   # expected packet number 
        self.packet_number = 1      # packet count

    def receive_data(self):
        while True:
            # waiting for the message from sender
            data_packet, addr = self.receiver_socket.recvfrom(1024)
            print("packet num.{} received: {}".format(self.packet_number,data_packet))
            # simulating packet loss by triggering sleep when packet number is divisible by 6
            if self.packet_number % 6 == 0:
                print("simulating packet loss: sleep a while to trigger timeout event on the send side...")
                sleep(3)
                print("all done for this packet!")
                self.packet_number += 1
                print("\r\n\r\n")
                return

            # simulating corrupt packet by sending the previous sequence number when packet number is divisible 3
            if self.packet_number % 3 == 0:
                print("simulating packet bit errors/corrupted: ACK the previous packet!")
                ack_packet = make_packet("", 1, (1 - self.expected_seq_num))
                self.receiver_socket.sendto(ack_packet, addr)
                # self.expected_seq_num = 1 - self.expected_seq_num
                print("all done for this packet!")
                self.packet_number += 1
                print("\r\n\r\n")
                return
  
            # verifies checksum and sequence number
            if verify_checksum(data_packet) and seq_number_of_packet(data_packet) == self.expected_seq_num:
                message = msg_retrieve(data_packet)
                print("packet is expected, message string delievered: {}".format(message))
                print("packet is delivered, now creating and sending the ACK packet...")
                ack_packet = make_packet("", 1, self.expected_seq_num)
                self.receiver_socket.sendto(ack_packet, addr)
                self.expected_seq_num = 1 - self.expected_seq_num
                print("all done for this packet!")
                self.packet_number += 1
                print("\r\n\r\n")
                return message


if __name__ == "__main__":
    receiver = Receiver(10145)
    while True:
        receiver.receive_data()