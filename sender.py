from socket import *
from util import *

'''Directions to run: Please start up receiver.py first. Then main.py. '''

class Sender:
  def __init__(self):
        """ 
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()
        
        Please check the main.py for a reference of how your function will be called.
        """
        self.receiver_host = '127.0.0.1'   # receiver address
        self.receiver_port = 10145         # receiver port
        self.sender_socket = socket(AF_INET, SOCK_DGRAM)      # sender socket
        self.seq_num = 0                  # sequence number of the packet
        self.packet = None                # packet 
        self.acknowledged = False         # acknowledgement status
        self.data = None                  # message
        self.packet_number = 1            # packet count
        


  def rdt_send(self, app_msg_str):
      """realibly send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)

      Args:
        app_msg_str: the message string (to be put in the data field of the packet)

      """
      # getting the message as a function argument
      self.data = app_msg_str

      print("Original message string: {}".format(self.data))

      # function call for creating the packet
      self.packet = make_packet(self.data, 0, self.seq_num)
      print("packet created: {}".format(self.packet))

      self.acknowledged = False
      while not self.acknowledged:
        # sending the packet to receiver
        self.sender_socket.sendto(self.packet, (self.receiver_host, self.receiver_port))
        print("packet num.{} is successfully sent to the receiver.".format(self.packet_number))
        # setting the timeout for retransmission
        self.sender_socket.settimeout(2)
        try:
          # waiting for the ack from receiver
          ack_packet, addr = self.sender_socket.recvfrom(1024)
        except timeout:
          # retransmission of the previous packet
          print("socket timeout! Resend!")
          print("\r\n\r\n")
          print("[timeout retransmission]: {}".format(self.data))
          self.packet_number += 1
          self.sender_socket.sendto(self.packet, (self.receiver_host, self.receiver_port))
          print("packet num.{} is successfully sent to the receiver.".format(self.packet_number))
          # waiting for the ack from receiver
          ack_packet, addr = self.sender_socket.recvfrom(1024)

        # verifies the checksum and checks the ack bit and verifies the sequence number
        if verify_checksum(ack_packet) and is_ack(ack_packet) and seq_number_of_packet(ack_packet) == self.seq_num:
          self.seq_num = 1 - self.seq_num
          self.acknowledged = True
          print("packet is received correctly: seq num {} = ACK num {}. all done!".format(self.seq_num,self.seq_num))
          print("\r\n\r\n")
        else:
          # receives corrupted ack packet from the receiver
          print("receiver acked the previous pkt, resend!")
          print("\r\n\r\n")
          print("[ACK-Previous retransmission]: {}".format(self.data))
          self.packet_number += 1
          self.sender_socket.sendto(self.packet, (self.receiver_host, self.receiver_port))
          print("packet num.{} is successfully sent to the receiver.".format(self.packet_number))
          ack_packet, addr = self.sender_socket.recvfrom(1024)
          if verify_checksum(ack_packet) and is_ack(ack_packet) and seq_number_of_packet(ack_packet) == self.seq_num:
            self.seq_num = 1 - self.seq_num
            self.acknowledged = True
            print("packet is received correctly: seq num {} = ACK num {}. all done!".format(self.seq_num,self.seq_num))
            print("\r\n\r\n")
        # incrementing the packet number after transmission
        self.packet_number += 1
        

      

  ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
  ####### function, which will be called by an application to                 #######
  ####### send a message. DO NOT change the function name.                    #######                    
  ####### You can have other functions if needed.                             #######   