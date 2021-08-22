from core.persist import session
from core.exceptions import ClientEx
from entities.exit import Exit
from entities.room import Room


class ExitService:
    def __init__(self):
        self.session = session

    def create(self, char, name):
        exit = Exit(name=name, owner=char, exit=char.room)

        self.session.add(exit)
        self.session.commit()
        return exit

    def set_property(self, char, id, key, value):
        exit = self.session.query(Exit).filter(Exit.id == id).one_or_none()

        if exit == None: raise ClientEx("Exit not found with id: {}".format(id))

        if key == "name":
            exit.name = value
        elif key == "entry_id":
            room = self.session.query(Room).filter(Room.id == value).one_or_none()
            if room == None: raise ClientEx("Entry for room not found with id: {}".format(id))

            exit.entry = room
        elif key == "desc":
            exit.desc = value
        else:
            raise ClientEx("Invalid property: {} (Available: name, entry_id, desc)".format(key))

        self.session.commit()


exit_service = ExitService()
