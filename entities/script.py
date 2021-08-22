from functools import partial

from core.utils import prn
from core.persist import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, event
from sqlalchemy.orm import relationship

# Many to Many requirements
from entities.script_to_room import ScriptToRoom
from entities.script_to_exit import ScriptToExit

from cmud import exec, create_blank_env, load_str

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

    async def run_in_room_enter(self):
        pass

    async def run_in_room_leave(self, room, char):
        pass

    async def run_in_exit(self, ws, user, room_origin, room_dest):
        if self.hooks and hasattr(self.hooks, 'run_in_exit'):
            tools = { 
                    "echo": partial(prn, ws),
            }
            char = { "name": user.name, "id": user.id }

            return await self.hooks.run_in_exit(tools, char)
        else:
            return True

    async def run_on_use(self, char, cmd):
        pass

    async def run_on_char(char, cmd):
        pass

def on_load(target, context):
    if target.code:
        env = create_blank_env()

        load_str("(defmacro! defun (fn* [name args func] `(def! ~name (fn* ~args ~func))))", env)
        load_str("(defmacro! . (fn* [tools key & args] `(~key ~tools ~@args)))", env)

        try:
            target.hooks = exec(env, "(do" + target.code.decode("utf-8") + ")")
        except Exception as e:
            print(e)
            target.error = str(e)
            target.hooks = None

event.listen(Script, 'load', on_load)

