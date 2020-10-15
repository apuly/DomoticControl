from enum import Enum, auto

CMD_ID_SIZE = 2 #length of command ID is 2 bytes
FRAME_LENGTH_SIZE = 2 #16 bit frame length identifier
TIMESTAMP_SIZE = 8 #64 bit unix timestamp
UUID_SIZE = 8 #64 bit device IDS
DEVICE_TYPE_SIZE = 2 #16 bit device type identifier
PROTOCOL_SIZE = 1 #8 protocol identifier


class to_dc(Enum):
    REQUEST_ID = 0
    REQUEST_INFO = 1
    MODULE_INFO = 2
    SEND_VALUE = 3 

class from_dc(Enum):
    SET_ID = 0
    SEND_INFO = 1 