from core.utils import read_command, prn

from core.exceptions import ClientEx

from service.script import script_service

async def script(ws, user, data):
    if data["type"] == "copy_script":    # Copy script
        pass
    if data["type"] == "detach_script":  # detach script from obj/room/char
        pass
    if data["type"] == "attach_script":  # attach script to obj/room/char
        await attach(ws, user, data)


async def attach(ws, user, data):
    if len(data["content"]) != 3:
        raise ClientEx("Invalid arguments: /attach_script script_id [room|exit|object] target_id")

    args = data["content"]

    script_service.attach_script(user, args[0], args[1], args[2])
    await prn(ws, "Script attached to {} with id {}".format(args[1], args[2]))

