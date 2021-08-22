from core.utils import read_command, prn
from core.exceptions import ClientEx

from service.script import script_service
from service.room import room_service
from service.exit import exit_service


async def build(ws, char, data):
    if data["type"] == "chown":  pass
    if data["type"] == "chmod":  pass
    if data["type"] == "delete": pass
    if data["type"] == "eval":   pass
    if data["type"] == "list":   await build_list(ws, char, data)
    if data["type"] == "create": await build_create(ws, char, data)
    if data["type"] == "set":    await build_set(ws, char, data)

async def build_list(ws, char, data):
    if len(data["content"]) != 1:
        raise ClientEx("Invalid arguments: /list [room|exit|script|object]")
    else:
        args = data["content"]

        if args[0] == "room":
            await prn(ws, "Owned rooms:")
            for room in char.rooms:
                await prn(ws, "\t- [#{}] {}".format(room.id, room.name))
        elif args[0] == "exit":
            await prn(ws, "Owned exits:")
            for exit in char.exits:
                await prn(ws, "\t- [#{}] {}".format(exit.id, exit.name))
        elif args[0] == "script":
            await prn(ws, "Owned scripts:")
            for script in char.scripts:
                await prn(ws, "\t- [#{}] {}".format(script.id, script.name))
        elif args[0] == "object":
            pass
        else:
            raise ClientEx("Invalid arguments: /list [room|exit|script|object]")

async def build_create(ws, char, data):
    if len(data["content"]) != 2:
        raise ClientEx("Invalid arguments: /create [room|exit|script|object] <name>")
    else:
        args = data["content"]

        if args[0] == "room":
            room = room_service.create(char, args[1])
            await prn(ws, "Room created with id: {}".format(room.id))
        elif args[0] == "exit":
            exit = exit_service.create(char, args[1])
            await prn(ws, "Exit created with id: {}".format(exit.id))
        elif args[0] == "script":
            script = script_service.create(char, args[1])
            await prn(ws, "Script created with id: {}".format(script.id))
        elif args[0] == "object":
            pass
        else:
            raise ClientEx("Invalid arguments: /create [room|script|exit|object] <name>")


async def build_set(ws, char, data):
    if len(data["content"]) != 4:
        raise ClientEx("Invalid arguments: /set [room|script|exit|object] <id> <property> <value>")
    else:
        args = data["content"]

        if args[0] == "room":
            room_service.set_property(char, *args[1:])
            await prn(ws, "Room updated")
        elif args[0] == "exit":
            exit_service.set_property(char, *args[1:])
            await prn(ws, "Exit updated")
        elif args[0] == "script":
            script_service.set_property(char, *args[1:])
            await prn(ws, "Script updated")
        elif args[0] == "object":
            pass
        else:
            raise ClientEx("Invalid arguments: /set [room|exit|script|object] <id> <property> <value>")


