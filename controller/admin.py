from core.utils import read_command, prn

from core.exceptions import ClientEx


async def admin(ws, data):
    if data["type"] == "ban":    # Ban a user
        pass
    if data["type"] == "priv":    # Change user privilege
        pass
