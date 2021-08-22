from core.persist import session
from entities.room import Room

from core.utils import prn
from core.exceptions import ClientEx

class RoomService():
    def __init__(self):
        self.session = session

    def create(self, char, name):
        room = Room(name=name, owner=char)

        self.session.add(room)
        self.session.commit()
        return room

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

    async def look_user_room(self, ws, char):
        room = char.room
        await prn(ws, room.desc)
        for exit in room.exits:
            await prn(ws, "{} (Exit: #{})".format(exit.desc or exit.name or "exit", exit.id))
        # Add players

    def init(self):
        if self.session.query(Room).count() == 0:
            r = Room(name="spawn",
                     spawn=True,
                     desc="You are in the spawn room, it's an empty white room.")

            self.session.add(r)
            self.session.commit()


room_service = RoomService()
