import json
import os 
from pkg_resources._vendor.jaraco.text import indent

CONFIG_PATH = "/config.json"


class Relay():
    
    def __init__(self, path="./cetd"):
        self.path = path
        self.is_initialized = False
        self.network = 'main'
        self.name = 'No Name'
        self.description = 'A CSC relay node'
        self.load()
    
    def load(self):
        path = self.path + CONFIG_PATH
        if not os.path.isfile(path):
            self.is_initialized = False
            return
        with open(path, 'r') as file:
            map = json.load(file)
            for key in map:
                self.set(key, map.get(key))
    
    def save(self):
        path = self.path + CONFIG_PATH
        with open(path, 'w') as file:
            json.dump(self.__dict__, file, indent=4)
    
    def __setattr__(self, key, value):
        self.__dict__[key] = value
        return value
    
    def set(self, key, value):
        return self.__setattr__(key, value)
    
    def __getattr__(self, key):
        return self.get(key)
    
    def get(self, key, default=None):
        if key in self.__dict__:
            return self.__dict__[key]
        return default
    
    def __str__(self):
        return json.dumps(self.__dict__, indent=4)

    
def is_relay_node(path):
    if not os.path.exists(path):
        return False
    
    path = path + CONFIG_PATH
    if not os.path.isfile(path):
        return False
    
    # TODO: maso, 2022: add more condition to check if it is a relay node
    return True


def create_relay_node(path):
    """ Creates new Relay object
    
    Relay object point to a relay node with configuration and related
    configs. This function create a new relay and return it as result.
    """
    # create folder if not exist
    if not os.path.isdir(path):
        os.mkdir(path)
    
    relay = Relay(
        path=path
    )
    return relay

