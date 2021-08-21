from core.persist import session
from entities.room import Room

class RoomService():
    def __init__(self):
        self.session = session

    def list(self, char):
        return char.rooms

    def create(self, char, name):
        room = Room(name=name, owner=char)

        self.session.add(room)
        self.session.commit()
        return script

    def set_property(self, char, id, key, value):
        room = self.session.query(Room).filter(Room.id == id).one_or_none()

        if room == None: raise ClientEx("Room not found with id: {}".format(id))

        if key == "name":
            room.name = value
        elif key == "desc":
            room.desc = value
        else:
            raise ClientEx("Invalid property: {} (Available: name, desc)".format(key))

        self.session.commit()

    def init(self):
        if self.session.query(Room).count() == 0:
            r = Room(name="spawn",
                     spawn=True,
                     desc="You are in the spawn room, it's an empty white room.")

            self.session.add(r)
            self.session.commit()


room_service = RoomService()
