from core.persist import Base, session
from entities.script import Script

class ScriptService:
    def __init__(self):
        self.session = session

    def set_property(self, id, key, value):
        char = self.session.query(Script).filter(Script.id == id).one_or_none()

        if char == None: raise ClientEx("Script not found with id: {}".format(id))

        if key == "name":
            char.name = value
        elif key == "code":
            char.code = value
        else:
            raise ClientEx("Invalid property: {}".format(key))

        self.session.commit()


    def create(self, char, name):
        script = Script(name=name, owner=char)

        self.session.add(script)
        self.session.commit()
        return script


script_service= ScriptService()
