from core.utils import read_command, prn

from core.exceptions import ClientEx


async def script(ws, data):
    if data["type"] == "copy_script":    # Copy script
        pass
    if data["type"] == "detach_script":  # detach script from obj/room/char
        pass
    if data["type"] == "attach_script":  # attach script to obj/room/char
        pass
