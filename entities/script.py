from core.persist import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, event
from sqlalchemy.orm import relationship

# Many to Many requirements
from entities.script_to_room import ScriptToRoom
from entities.script_to_exit import ScriptToExit

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
    exits = relationship('Exit', secondary = 'script_to_exit')

    async def run_in_room(self, ws, name):
        rt = LuaRuntime(unpack_returned_tuples=True)
        fncs = rt.eval(self.code)
        if run != None:
            pass

    def run_in_room_enter(self):
        pass

    def run_in_room_leave(self, room, char):
        pass

    def run_in_exit(self, char, origin, dest):
        pass

    def run_on_use(self, char, cmd):
        pass

    def run_on_char(char, cmd):
        pass

def on_load(target, context):
    rt = LuaRuntime(unpack_returned_tuples=True)
    #lua = lupa.LuaRuntime(attribute_handlers=(getter, setter))
    if target.code:
        try:
            target.hooks = rt.eval(target.code.decode("utf-8"))
        except Exception as e:
            print(e)
            target.error = str(e)
            target.hooks = None

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
"""


