from core.persist import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, event
from sqlalchemy.orm import relationship

# Many to Many requirements
from entities.script_to_room import ScriptToRoom

import lupa
from lupa import LuaRuntime

class Script(Base):
    __tablename__ = 'script'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    perms = Column(Integer)
    code = Column(String)

    owner_id = Column(Integer, ForeignKey('character.id'))
    owner = relationship("Character", back_populates="scripts")

    rooms = relationship('Room', secondary = 'script_to_room')

    async def run_in_room(self, ws, name):
        rt = LuaRuntime(unpack_returned_tuples=True)
        fncs = rt.eval(self.code)
        if run != None:
            return fncs.run_in_room(ws, name)


def on_load(target, context):
    rt = LuaRuntime(unpack_returned_tuples=True)
    target.hooks = rt.eval(target.code)

event.listen(Script, 'load', on_load)



"""
getter(obj, attr_name):
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

class X(object)
     yes = 123
     put = 'abc'
     noway = 2.1

x = X()

lua = lupa.LuaRuntime(attribute_handlers=(getter, setter))
"""


