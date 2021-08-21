from core.utils import read_command, prn

from core.exceptions import ClientEx


async def room(ws, user, data):
    if data["type"] == "link": # Link a room to another one
        pass
