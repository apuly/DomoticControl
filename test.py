import socket
from time import sleep
from protocols.v1 import domoticcom
from protocols.v1 import packets

class tester():
    VERSION = 1 #version of the protocol this test is writtten for

    MODULE_TYPE = 0
    time = None
    uuid = None
    dcid = None

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def build_base_frame(self, command, args=b''):
        length = 5+len(args)
        version_bytes = self.VERSION.to_bytes(1, 'big')
        cmd_bytes = command.to_bytes(2, 'big')
        len_bytes = length.to_bytes(2, 'big')
        return version_bytes+len_bytes+cmd_bytes+args

    def build_module_frame(self, command, args = b''):
        uuid_bytes = self.uuid.to_bytes(8, 'big')
        self.build_base_frame(command, uuid_bytes+args)

    def send(self, msg):
        if isinstance(msg, packets.base_packet):
            msg = msg.serialize()
            #print(msg)
        self.sock.sendall(msg)

    def test(self):
        msg = packets.request_id()
        self.send(msg)
        self.recv_response()
        msg = packets.request_info()
        self.send(msg)
        self.recv_response()
        packet = packets.module_info(self.uuid, self.MODULE_TYPE)
        self.send(packet)
        sleep(0.01) #give server some time to handle data
        packet = packets.send_value(self.uuid, (1700).to_bytes(2, 'big'))
        self.send(packet)
        #self.recv_response()
        sleep(2)
        self.send(b"shutdownowplzuwu")



    def recv_response(self):
        length = int.from_bytes(self.sock.recv(2), 'big')
        version = self.sock.recv(1)
        cmd = int.from_bytes(self.sock.recv(2), 'big')
        length -= 4
        rest = self.sock.recv(length)
        if cmd == domoticcom.from_dc.SET_ID.value:
            self.handle_set_id(length, rest)
        elif cmd == domoticcom.from_dc.SEND_INFO.value:
            self.handle_send_info(length, rest)

    def handle_send_info(self, dat_len, rest):
        self.dcid = int.from_bytes(rest[:8], 'big')
        self.time = int.from_bytes(rest[8:], 'big')
        print(f"Received info: time {self.time}, id {self.dcid}") 


    def handle_set_id(self, dat_len, rest):
        self.uuid = int.from_bytes(rest, 'big')
        print(f"Received ID {self.uuid}")