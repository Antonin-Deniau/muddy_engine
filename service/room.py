from core.persist import session
from entities.room import Room

class RoomService():
    def __init__(self):
        self.session = session

    def init(self):
        if self.session.query(Room).count() == 0:
            r = Room(name="spawn",
                     spawn=True,
                     desc="You are in the spawn room, it's an empty white room.",
                     code="")

            self.session.add(r)
            self.session.commit()


room_service = RoomService()
