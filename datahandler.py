#import packets.base_protocol as packets
from lib.uuid64 import uuid64
import ctypes
import time
import struct

from protocols.v1.protocol import protocol as protocol_v1

#number of bytes that indicate the length of a packet
#actual number of bytes will be limited to 384 bytes as per bluetooth mesh specification
FRAME_LENGTH_SIZE = 2 

class DataHandler():
    def __init__(self, dc_info):
        self._info = dc_info
        self._protocols = [protocol_v1(dc_info)]

    def handle(self, data):
        version = data[0]-1
        del data[0]

        frame_length = data[:FRAME_LENGTH_SIZE]
        frame_length = int.from_bytes(frame_length, 'big')
        del data[:FRAME_LENGTH_SIZE]
        # print("version: ", version)
        # print("length: ", frame_length)
        
        #after protocol and frame length have been grabbed, data can be
        #passed to correct protocol handler
        protocol = self._protocols[version]
        return protocol.handle(frame_length, data)
