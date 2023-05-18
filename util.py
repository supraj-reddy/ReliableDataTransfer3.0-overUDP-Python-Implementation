def create_checksum(packet_wo_checksum):
    """create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet_wo_checksum: the packet byte data (including headers except for checksum field)

    Returns:
      the checksum in bytes

    """
    # Pad the data with a zero byte if its length is odd
    if len(packet_wo_checksum) % 2 == 1:
        packet_wo_checksum += b' '
    
    # Calculate the checksum using 16-bit ones' complement arithmetic
    checksum = 0
    for i in range(0, len(packet_wo_checksum), 2):
        word = (packet_wo_checksum[i] << 8) + packet_wo_checksum[i+1]
        # print(word.to_bytes(2,byteorder="big"))
        checksum += word
        if checksum > 0xffff:
            checksum = (checksum & 0xffff) + 1
    
    # Take the ones' complement of the sum
    checksum = ~checksum & 0xffff
    
    return checksum

def verify_checksum(packet):
    """verify packet checksum (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet: the whole (including original checksum) packet byte data

    Returns:
      True if the packet checksum is the same as specified in the checksum field
      False otherwise

    """
    # Extract the checksum from the packet (bytes 9 and 10)
    checksum = int.from_bytes(packet[8:10], byteorder='big')

    # Calculate the checksum over the rest of the packet (bytes 0-8 and 10-end)
    packet_data = packet[:8] + packet[10:]
    calculated_checksum = create_checksum(packet_data)

    # Compare the extracted checksum with the calculated checksum
    return checksum == calculated_checksum

def make_packet(data_str, ack_num, seq_num):
    """Make a packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      data_str: the string of the data (to be put in the Data area)
      ack: an int tells if this packet is an ACK packet (1: ack, 0: non ack)
      seq_num: an int tells the sequence number, i.e., 0 or 1

    Returns:
      a created packet in bytes

    """
    # make sure your packet follows the required format!
    # encode the string to bytes
    data = data_str.encode("UTF-8")

    # Calculating the packet length
    packet_length = 12 + len(data)

    packet_fields = bytearray()
    packet_fields.extend(b'COMPNETW') # 8-byte headers
    packet_fields.extend(b'\x00\x00') # 2-byte placeholders for the checksum
    packet_fields.extend(b'\x00') # 2-byte packet length, ack number and seq. num
    
    packet_length = packet_length << 2 # bitwise leftshift
    if ack_num == 1:
      packet_length += 2 
    if seq_num == 1:
      packet_length += 1
    
    packet_fields.extend(chr(packet_length).encode())
    packet_fields.extend(data)

    # Calculate the UDP checksum and replace the placeholder
    checksum = create_checksum(packet_fields)
    packet_fields[8:10] = checksum.to_bytes(2, byteorder='big')
    
    return bytes(packet_fields)


def msg_retrieve(packet):
    """Retrieve msg from the received packet

    Args:
      packet: packet containing the actual message

    Returns:
      message string

    """
    message = packet[12:].decode()
    return message

def is_ack(packet):
    """Check the received packet for ACK bit

    Args:
      packet: packet containing the actual message

    Returns:
      True if ack bit is set to 1

    """
    ack_byte = packet[11:12].decode()
    if ord(ack_byte) & 0b00000011 == 3 or ord(ack_byte) & 0b00000011 == 2:
      return True
    else:
      return False

def seq_number_of_packet(packet):
    """Check the received packet for seq num

    Args:
      packet: packet containing the actual message

    Returns:
      Sequence Number of the packet

    """
    seq_byte = packet[11:12].decode()
    if ord(seq_byte) & 0b00000011 == 3 or ord(seq_byte) & 0b00000011 == 1:
      seq_number = 1
    else:
      seq_number = 0

    return seq_number


###### These three functions will be automatically tested while grading. ######
###### Hence, your implementation should NOT make any changes to         ######
###### the above function names and args list.                           ######
###### You can have other helper functions if needed.                    ######  
