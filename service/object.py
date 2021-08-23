from core.persist import session
from core.exceptions import ClientEx
from entities.object import Object


class ObjectService:
    def __init__(self):
        self.session = session

    def create(self, char, name):
        obj = Object(name=name, owner=char, holder=char)

        self.session.add(obj)
        self.session.commit()
        return obj

    def set_property(self, char, id, key, value):
        obj = self.session.query(Object).filter(Object.id == id).one_or_none()

        if obj == None: raise ClientEx("Object not found with id: {}".format(id))

        if key == "name":
            obj.name = value
        elif key == "desc":
            obj.desc = value
        else:
            raise ClientEx("Invalid property: {} (Available: name, desc)".format(key))

        self.session.commit()


object_service = ObjectService()
