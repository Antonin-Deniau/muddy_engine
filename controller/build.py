from core.utils import read_command, prn
from core.exceptions import ClientEx

from service.script import script_service


async def build(ws, char, data):
    if data["type"] == "chown":  pass
    if data["type"] == "chmod":  pass
    if data["type"] == "delete": pass
    if data["type"] == "rename": pass
    if data["type"] == "list":   await build_list(ws, char, data)
    if data["type"] == "create": await build_create(ws, char, data)
    if data["type"] == "set":    await build_set(ws, char, data)

async def build_list(ws, char, data):
    if len(data["content"]) != 1:
        raise ClientEx("Invalid arguments: /list [room|script|object]")
    else:
        args = data["content"]

        if args[0] == "room":
            pass
        elif args[0] == "script":
            scripts = script_service.list(char)

            await prn(ws, "Owned scripts:")
            for script in scripts:
                await prn(ws, "\t- [#{}] {}".format(script.id, script.name))
        elif args[0] == "object":
            pass
        else:
            raise ClientEx("Invalid arguments: /list [room|script|object]")

async def build_create(ws, char, data):
    if len(data["content"]) != 2:
        raise ClientEx("Invalid arguments: /create [room|script|object] <name>")
    else:
        args = data["content"]

        if args[0] == "room":
            pass
        elif args[0] == "script":
            script = script_service.create(char, args[1])
            await prn(ws, "Script created with id: {}".format(script.id))
        elif args[0] == "object":
            pass
        else:
            raise ClientEx("Invalid arguments: /create [room|script|object] <name>")


async def build_set(ws, char, data):
    if len(data["content"]) != 4:
        raise ClientEx("Invalid arguments: /set [room|script|object] <id> <property> <value>")
    else:
        args = data["content"]

        if args[0] == "room":
            pass
        elif args[0] == "script":
            script_service.set_property(char, *args[1:])
            await prn(ws, "Script updated")
        elif args[0] == "object":
            pass
        else:
            raise ClientEx("Invalid arguments: /set [room|script|object] <id> <property> <value>")
