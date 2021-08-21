from core.persist import session
from entities.room import Room

class RoomService():
    def __init__(self):
        self.session = session

    def init(self):
        if self.session.query(Room).count() == 0:
            r = Room(name=name,
                     desc=nick,
                     code=user)

            self.session.add(r)
            self.session.commit()


room_service = RoomService()
