from core.persist import Base
from sqlalchemy import Column, Integer, String, ForeignKey

import lupa
from lupa import LuaRuntime

class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    code = Column(String)

    parent_id = Column(Integer, ForeignKey('room.id'))
    parent = relationship("Room", back_populates="rooms")
    rooms = relationship("Room", back_populates="parent")

    # Transcient properties
    def __init__(self, **kwargs):
        self.rt = LuaRuntime(unpack_returned_tuples=True)

        self.code = kwargs["code"]
        self.name = kwargs["name"]
        self.desc = kwargs["desc"]
        self.parent_id = kwargs["parent_id"]
        self.parent = kwargs["parent"]
        self.rooms = kwargs["rooms"]

    def exec(self, ws, name):
        run = self.rt.eval(self.code)

        return run(ws, name)
