#!/usr/bin/python3

from simple_plugin_loader import Loader
from . import base_plugin
import os

class PluginManager():
    _loaded = False
    _plugins = {}
    def __init__(self, dc):
        self._dc = dc
        self._loader = Loader()

    def init_plugins(self, path="plugins", base=base_plugin.DomoticPlugin, recursive=True):
        plugins = self._loader.load_plugins(path, base, recursive)
        for plugin in plugins:
            plugins[plugin] = plugins[plugin](self._dc)
        self._plugins = plugins
        print(self._plugins)

    def get_plugin_by_name(self, name):
        if name in self._plugins:
            return self._plugins[name]