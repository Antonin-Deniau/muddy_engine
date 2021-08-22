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


loop = asyncio.get_event_loop()

# Non blocking events
def wait_queue(future, x):
    future.set_result(x.get())

async def wait_for_event():
    future = loop.create_future()

    loop.call_soon(wait_queue, future, q)

    return await future


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

    async def run_on_exit(self, ws, user, room_origin, room_dest):
        print("MAY SCRIPT")
        if self.code == None: return True
        if self.hooks == None: self.populate()

        print("MAY TRIGGER SCRIPT")
        if self.hooks and hasattr(self.hooks, 'run_on_exit'):
            print("TRIGGER SCRIPT")
            queue = multiprocessing.Queue()

            char = { "name": user.name, "id": user.id }
            tools = { 
                "echo": lambda e: queue.put(["echo", e]),
                "done": lambda e=True: queue.put(["done", e]),
            }


            p = multiprocessing.Process(target=self.hooks.run_on_exit, args=(tools, char,))
            p.start()

            while True:
                data = await wait_for_event()

                print("Entry", data)
                if data == None:
                    print("Returning true")
                    return True

                event = data[0]
                args = data[1:]

                if event == "echo":
                    await prn(ws, args[0])
                if event == "done":
                    print("Returning res")
                    return args[0]

            queue.close()
            queue.join_thread()
            p.join()
            return True
        else:
            return True

    async def run_on_use(self, char, cmd):
        pass

    async def run_on_char(char, cmd):
        pass

    def populate(self):
        if self.code:
            env = create_blank_env()

            load_str("(defmacro! defun (fn* [name args func] `(def! ~name (fn* ~args ~func))))", env)
            load_str("(defmacro! # (fn* [tools key & args] `(~key ~tools ~@args)))", env)

            try:
                self.hooks = exec("(do " + self.code.decode("utf-8") + "\n)", env)
                print("POPULATED HOOKS")
                print("POPULATED HOOKS")
                print("POPULATED HOOKS")
                print("POPULATED HOOKS")
            except Exception as e:
                traceback.print_exc()
                print(e)
                self.error = str(e)
                self.hooks = None

