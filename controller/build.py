from core.utils import read_command, prn
from core.exceptions import ClientEx

from service.script import script_service


async def build(ws, user, data):
    if data["type"] == "chown":  pass
    if data["type"] == "chmod":  pass
    if data["type"] == "delete": pass
    if data["type"] == "rename": pass
    if data["type"] == "create": async build_create(ws, user, data)
    if data["type"] == "set":    async build_set(ws, user, data)


async build_create(ws, user, data):
    if len(data["content"]) != 2:
        raise ClientEx("Invalid arguments: /create [room|script|object] <name>")
    else:
        if data["content"][0] == "room":
            pass
        elif data["content"][0] == "script":
            #script_service.create()
            pass
        elif data["content"][0] == "object":
            pass
        else:
            raise ClientEx("Invalid arguments: /set [room|script|object] <property> <value>")


async def build_set(ws, user, data):
    if len(data["content"]) != 3:
        raise ClientEx("Invalid arguments: /set [room|script|object] <property> <value>")
    else:
        if data["content"][0] == "room":
            pass
        elif data["content"][0] == "script":
            #script_service.set_property()
            pass
        elif data["content"][0] == "object":
            pass
        else:
            raise ClientEx("Invalid arguments: /set [room|script|object] <property> <value>")
