from functools import partial
import multiprocessing
import traceback


from core.utils import prn
from core.persist import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, event
from sqlalchemy.orm import relationship

# Many to Many requirements
from entities.script_to_room import ScriptToRoom
from entities.script_to_exit import ScriptToExit

from cmud.cmud import exec, create_blank_env, load_str


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

    async def run_on_room_enter(self, ws, room, char):
        pass

    async def run_on_room_leave(self, ws, room, char):
        pass

    async def run_on_exit(self, ws, user):
        if self.code == None: return True
        if not hasattr(self, "hooks"): await self.populate()

        if self.hooks and hasattr(self.hooks, 'run_on_exit'):
            char = { "name": user.name, "id": user.id }
            tools = { 
                "echo": lambda e: prn(ws, e),
            }

            return await self.hooks.run_on_exit(tools, char)
        else:
            return True

    async def run_on_use(self, char, cmd):
        pass

    async def run_on_char(char, cmd):
        pass

    async def populate(self):
        if self.code:
            env = create_blank_env()

            await load_str("(defmacro! defun (fn* [name args func] `(def! ~name (fn* ~args ~func))))", env)
            await load_str("(defmacro! # (fn* [tools key & args] `(~key ~tools ~@args)))", env)

            try:
                self.hooks = await exec("(let* [] (do " + self.code.decode("utf-8") + "\n))", env)
            except Exception as e:
                traceback.print_exc()
                print(e)
                self.error = str(e)
                self.hooks = None

