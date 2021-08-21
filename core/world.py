import yaml, os, glob

from core.exceptions import ClientEx
from entities.container import Container
from entities.room import Room

yaml.warnings({'YAMLLoadWarning': False})

class World():
    def __init__(self, name):
        self.name = {}

    def get_room(self, name):
        pass
