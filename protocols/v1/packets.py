#!/usr/bin/python3

#module containing the different packets that are used for communcation

import enum
from . import domoticcom


class base_packet():
    def __init__(self, cmd_id: int, data=b''):
        if isinstance(cmd_id, enum.Enum): #automatically convert from enum
            self._id = cmd_id.value
        else:
            self._id = cmd_id

        #I would not advice just plonking any data in here.
        #you lose a bit of control due to the automatic conversion
        #savest bet it just putting a byte array here, seeing as it doesn't get modified
        self._data = self.object_to_bytes(data)

    def __repr__(self):
        l = domoticcom.CMD_ID_SIZE + len(self._data) + \
            domoticcom.FRAME_LENGTH_SIZE + domoticcom.PROTOCOL_SIZE
        data = {'command': self._id, 'length': l, 'version': 1, 'data': self._data}
        return str(data)

    def object_to_bytes(self, obj): #converts multiple types of data into byte arrays
        if isinstance(obj, bytes):
            return obj
        if isinstance(obj, str):
            return str.encode('utf-8')
        elif isinstance(obj, int):
            arr_len = len(bin(obj))-2
            obj.to_bytes(arr_len, 'big')

    def serialize(self, data=None): #used to change the object into a byte array
        data = data or self._data
        version_bytes = (1).to_bytes(1, 'big')
        frame_length = domoticcom.CMD_ID_SIZE + len(data) + \
            domoticcom.FRAME_LENGTH_SIZE + domoticcom.PROTOCOL_SIZE
        id_bytes = self._id.to_bytes(domoticcom.CMD_ID_SIZE, 'big')
        length_bytes = frame_length.to_bytes(domoticcom.FRAME_LENGTH_SIZE, 'big')
        result_bytes = version_bytes+length_bytes+id_bytes+data
        return result_bytes
        

class module_packet(base_packet):
    def __init__(self, cmd_id: int, uuid: int, data = b''):
        super().__init__(cmd_id, data)
        self._uuid = uuid        

    def serialize(self, data=None):
        data = data or self._data
        id_bytes = self._uuid.to_bytes(domoticcom.UUID_SIZE, 'big')
        return super().serialize(id_bytes+data)



### PACKETS GOING FROM MODULE TO DC

class request_id(base_packet):
    def __init__(self):
        super().__init__(domoticcom.to_dc.REQUEST_ID)

class request_info(base_packet):
    def __init__(self):
        super().__init__(domoticcom.to_dc.REQUEST_INFO)

class module_info(module_packet):
    
    def __init__(self, uuid, module_type):
        super().__init__(domoticcom.to_dc.MODULE_INFO, uuid)
        self._type = module_type

    def serialize(self):
        type_bytes = self._type.to_bytes(domoticcom.DEVICE_TYPE_SIZE, 'big')
        return super().serialize(type_bytes)

class send_value(module_packet):
    def __init__(self, uuid, value):
        super().__init__(domoticcom.to_dc.SEND_VALUE, uuid)
        self._value = value

    def serialize(self):
        value_bytes = self.object_to_bytes(self._value)
        return super().serialize(value_bytes)


### PACKETS GOING DC TO MODULE

class send_id(base_packet):
    def __init__(self, uuid: int):
        uuid_bytes = uuid.to_bytes(domoticcom.UUID_SIZE, 'big')
        super().__init__(domoticcom.from_dc.SET_ID, uuid_bytes)

class send_info(base_packet):
    def __init__(self, dc_id: int):
        self._dc_id = dc_id
        super().__init__(domoticcom.from_dc.SEND_INFO)

    def serialize(self):
        id_bytes = self._dc_id.to_bytes(domoticcom.UUID_SIZE, 'big')
        return super().serialize(id_bytes)