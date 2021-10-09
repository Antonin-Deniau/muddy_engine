import base64
import uuid

from core.persist import Base, session
from entities.script import Script

from core.exceptions import ClientEx
from entities.room import Room
from entities.exit import Exit

class ScriptService:
    def __init__(self):
        self.session = session

    def set_property(self, char, id, key, value):
        script = self.session.query(Script).filter(Script.id == id).one_or_none()

        if script == None: raise ClientEx("Script not found with id: {}".format(id))

        if key == "name":
            script.name = value
        elif key == "code":
            script.set_code(value)
        else:
            raise ClientEx("Invalid property: {} (Available: name, code)".format(key))

        self.session.commit()

    def attach_script(self, user, script_id, target_type, target_id):
        script = self.session.query(Script).filter(Script.id == script_id).one_or_none()
        if script == None: raise ClientEx("Script not found with id: {}".format(id))

        if target_type == "room":
            room = self.session.query(Room).filter(Room.id == target_id).one_or_none()
            if room == None: raise ClientEx("Room not found with id: {}".format(target_id))

            script.rooms.append(room)
            self.session.commit()
        if target_type == "exit":
            exit = self.session.query(Exit).filter(Exit.id == target_id).one_or_none()
            if exit == None: raise ClientEx("Exit not found with id: {}".format(target_id))

            script.exits.append(exit)
            self.session.commit()
        else:
            raise ClientEx("Invalid target {} (Available: room, exit)".format(target_type))
        

    def create(self, char, name):
        script = Script(name=name, owner=char, code_uuid=uuid.uuid4())

        self.session.add(script)
        self.session.commit()
        return script

script_service = ScriptService()
