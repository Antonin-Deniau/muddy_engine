import yaml, os, glob

from core.exceptions import ClientEx
from entities.container import Container
from entities.room import Room

yaml.warnings({'YAMLLoadWarning': False})

class World():
    def __init__(self, folder):
        self.rooms = {}
        self.potions = {}
        self.containers = {}
        self.metadata = {}

        for f in glob.glob('{}/**/*.yml'.format(os.path.abspath(folder)), recursive=True):
            self._load_yml_file(f)

    def _load_yml_file(self, f):
        data = yaml.load(open(os.path.abspath(f), "r"))

        for key, value in data.items():
            if key == "room":
                self._load_rooms(value)
                continue

            if key == "container":
                self._load_containers(value)
                continue

            if key == "metadata":
                self._load_metadata(value)

    def _load_rooms(self, rooms):
        for key, value in rooms.items():
            value["name"] = key
            value["world"] = self
            self.rooms[key] = Room(**value)

    def _load_containers(self, containers):
        for key, value in containers.items():
            value["name"] = key
            value["world"] = self
            self.containers[key] = Container(**value)

    def _load_metadata(self, metadata):
        for key, value in metadata.items():
            self.metadata[key] = value

    def get_location(self, loc):
        if loc in self.rooms.keys():
            return self.rooms[loc]

        if loc in self.containers.keys():
            return self.containers[loc]

        raise ClientEx("Unknown location: {}".format(loc))

    def get_metadata(self, key):
        if key in self.metadata.keys():
            return self.metadata[key]
        else:
            return None
