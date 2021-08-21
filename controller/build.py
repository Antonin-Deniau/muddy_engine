from core.utils import read_command, prn

from core.exceptions import ClientEx


async def build(ws, data):
    if data["type"] == "chown":   # Change owner of an object/room/script
        pass
    if data["type"] == "chmod":   # Change perms of an object/room/script
        pass
    if data["type"] == "delete":  # Delete a object/room/script
        pass
    if data["type"] == "rename":  # Rename a object/room/script
        pass
    if data["type"] == "create":  # Create an object/room/script
        pass
    if data["type"] == "set":     # Set a property of an object/room/script
        pass
