from simple_plugin_loader.sample_plugin import SamplePlugin
from simple_classproperty import classproperty
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import abc

class DomoticPlugin(SamplePlugin, abc.ABC):
    def __init__(self, dc):
        self._dc = dc
