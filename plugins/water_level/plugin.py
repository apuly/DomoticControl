#this plugin has been realised to deal with the data received from water level sensors

from simple_classproperty import classproperty
from pluginManager import base_plugin
from . import db_schema
from data.module_types import ModuleTypes

from main import DomoticProtocol
from data.module_types import ModuleTypes
from datetime import datetime
import time

class GroundWaterPlugin(base_plugin.DomoticPlugin):
    def __init__(self, dc: DomoticProtocol):
        super().__init__(dc)
        dc.observer.subscribe(ModuleTypes.GroundWaterSensor, self.on_module_receive)
        try:
            #print(dc.db.engine)
            self._db = db_schema.DBSchema(dc.db.uri) #it breaks here
        except Exception as e:
            print(e)
        
    def on_module_receive(self, data):
        now = datetime.now()
        sensor_value = int.from_bytes(data['raw_data'][:2], 'big')
        entry = self._db.GroundWater(time = now, value = sensor_value, sensor = data['uuid'])
        session = self._db.session()
        session.add(entry)
        session.commit()
        session.close()

        


