import time

#from data.db import Device, session
from lib.uuid64 import uuid64
from data.module_types import ModuleTypes

from . import domoticcom, frames, packets

to_dc = domoticcom.to_dc

class protocol(object):
    def __init__(self, dc):
        self._dc = dc

    def print_id(self, id):
        data = id.to_bytes(8, 'big')
        s = ".".join([str(b) for b in data])
        print(s)

    def handle(self, frame_length, data):
        id = data[:domoticcom.CMD_ID_SIZE]
        id = int.from_bytes(id, 'big')
        del data[:domoticcom.CMD_ID_SIZE]


        try:
            command = to_dc(id)
        except ValueError:
            print(f"ID {id} requested, but command doesn't exist")
            raise NotImplementedError
        else:
            frame = frames.FrameParser.parse(command, frame_length-5, data)
            print(frame)
            return self._handle_command(command, frame)


    def _handle_command(self, command, data):

        handler_name = f"handle_{command.name.lower()}"  
        try:
            handler = getattr(self, handler_name)
        except AttributeError:
            print(f"{command} not implemented!")
        else: 
            return handler(data)

    def handle_request_id(self, data):
        module_id = uuid64().int()
        packet = packets.send_id(module_id)
        return packet

    def handle_request_info(self, data):
        packet = packets.send_info(self._dc.info['ID'])
        return packet

    def handle_module_info(self, data):
        device_type = self._dc.db.Device
        s = self._dc.db.session()
        uuid = data["uuid"]
        resp = s.query(device_type).filter(device_type.uuid == uuid).count()
        if resp == 0: #if uuid not yet in database
            device = device_type(uuid = uuid, type= data["module_type"], protocol=1)
            s.add(device)
            s.commit()
        s.close()

    def handle_send_value(self, data):
        device_type = self._dc.db.Device
        session = self._dc.db.session()
        module_id = session.query(device_type.type).filter(device_type.uuid == data["uuid"]).one()[0]
        try:
            module_type = ModuleTypes(module_id)
        except ValueError:
            print(f"{module_id} not a valid module ID")
            return
        session.close()
        data["type"] = module_type
        self._dc.observer.send_message(module_type, data)
