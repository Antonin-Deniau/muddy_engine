from core.persist import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

import lupa
from lupa import LuaRuntime

"""
def getter(obj, attr_name):
     if attr_name == 'yes':
         return getattr(obj, attr_name)
     raise AttributeError(
         'not allowed to read attribute "%s"' % attr_name)

def setter(obj, attr_name, value):
     if attr_name == 'put':
         setattr(obj, attr_name, value)
         return
     raise AttributeError(
         'not allowed to write attribute "%s"' % attr_name)

class X(object):
     yes = 123
     put = 'abc'
     noway = 2.1

x = X()

lua = lupa.LuaRuntime(attribute_handlers=(getter, setter))
"""

class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    code = Column(String)
    spawn = Column(Boolean)

    parent_id = Column(Integer, ForeignKey('room.id'))
    parent = relationship("Room", remote_side=[id], backref='rooms')

    characters = relationship("Character", back_populates="room")

    # Transcient properties
    def __init__(self, **kwargs):
        self.code = kwargs["code"]
        self.name = kwargs["name"]
        self.desc = kwargs["desc"]
        self.spawn = kwargs["spawn"] if "spawn" in kwargs else False
        self.parent_id = kwargs["parent_id"] if "parent_id" in kwargs else None

    async def exec(self, ws, name):
        rt = LuaRuntime(unpack_returned_tuples=True)
        run = rt.eval(self.code)
        if run != None:
            return run(ws, name)


