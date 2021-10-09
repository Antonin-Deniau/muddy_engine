import os
import traceback

from core.utils import prn
from core.persist import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, event
from sqlalchemy.orm import relationship

# Many to Many requirements
from entities.script_to_room import ScriptToRoom
from entities.script_to_exit import ScriptToExit
from entities.script_to_object import ScriptToObject

from cmud.cmud import exec, create_blank_env, load_str, run_basl_fnc
from cmud.basl_types import Keyword


class Script(Base):
    __tablename__ = 'script'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    perms = Column(Integer)
    code_uuid = Column(String)

    owner_id = Column(Integer, ForeignKey('character.id'))
    owner = relationship("Character", back_populates="scripts")

    rooms = relationship('Room', secondary = 'script_to_room')
    exits = relationship('Exit', secondary = 'script_to_exit')
    objects = relationship('Object', secondary = 'script_to_object')

    async def run_on_room_enter(self, ws, user):
        if self.loaded: return True
        if not hasattr(self, "hooks"): await self.populate()

        if self.hooks and 'run_on_room_enter' in self.hooks:
            char = {
                Keyword("name"): user.name,
                Keyword("id"): user.id,
            }
            tools = { 
                Keyword("echo"): lambda e: prn(ws, e),
            }

            return await run_basl_fnc(self.hooks["run_on_room_enter"], (tools, char))
        else:
            return True

    async def run_on_room_leave(self, ws, user):
        if self.loaded: return True
        if not hasattr(self, "hooks"): await self.populate()

        if self.hooks and 'run_on_room_leave' in self.hooks:
            char = {
                Keyword("name"): user.name,
                Keyword("id"): user.id,
            }
            tools = { 
                Keyword("echo"): lambda e: prn(ws, e),
            }

            return await run_basl_fnc(self.hooks["run_on_room_leave"], (tools, char))
        else:
            return True

    async def run_on_exit(self, ws, user):
        if self.loaded: return True
        if not hasattr(self, "hooks"): await self.populate()

        if self.hooks and 'run_on_exit' in self.hooks:
            char = {
                Keyword("name"): user.name,
                Keyword("id"): user.id,
            }
            tools = { 
                Keyword("echo"): lambda e: prn(ws, e),
            }

            return await run_basl_fnc(self.hooks["run_on_exit"], (tools, char))
        else:
            return True

    async def run_on_use(self, user, cmd):
        if self.loaded: return True
        if not hasattr(self, "hooks"): await self.populate()

        if self.hooks and 'run_on_use' in self.hooks:
            char = {
                Keyword("name"): user.name,
                Keyword("id"): user.id,
            }
            tools = { 
                Keyword("echo"): lambda e: prn(ws, e),
            }

            return await run_basl_fnc(self.hooks["run_on_use"], (tools, char, cmd))
        else:
            return True

    async def run_on_char(user, cmd):
        if self.loaded: return True
        if not hasattr(self, "hooks"): await self.populate()

        if self.hooks and 'run_on_char' in self.hooks:
            char = {
                Keyword("name"): user.name,
                Keyword("id"): user.id,
            }
            tools = { 
                Keyword("echo"): lambda e: prn(ws, e),
            }

            return await run_basl_fnc(self.hooks["run_on_char"], (tools, char, cmd))
        else:
            return True

    def set_code(self, value):
        script_path = os.path.join(os.environ['SCRIPT_STORAGE_PATH'], self.code_uuid)
        script_file = open(script_path, mode='a')
        script_file.write(value)
        script_file.close()

    def get_code(self):
        script_path = os.path.join(os.environ['SCRIPT_STORAGE_PATH'], self.code_uuid)
        if not os.path.isfile(script_path):
            return None

        script_file = open(script_path, mode='r')
        script = script_file.read()
        script_file.close()
        return script

    async def populate(self):
        code = self.get_code()

        if code != None:
            env = create_blank_env()
            try:
                self.hooks = await exec("(do " + code + "\n)", env)
                self.loaded = True
            except Exception as e:
                traceback.print_exc()
                print(e)
                self.error = str(e)
                self.hooks = None

