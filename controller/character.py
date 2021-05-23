from core.utils import read_command, prn
from service.character import character_service

from core.exceptions import ClientEx


async def create_character(ws, user, content):
    if len(content) != 2: raise ClientEx("Invalid arguments: /create <name> <nick>")
    return character_service.create_character(content[0], content[1], user, "starting_hub", "starting_hub")

async def choose_character(ws, user, content):
    pass

async def manage_character(ws, user):
    while True:
        try:
            if len(user.characters) != 0:
                await prn(ws, "Please choose your character with \"/choose <name>\", or create one with \"/create <name> <nick>\": ")
                for char in user.characters:
                    await prn(ws, "\t- {}: {}".format(char.name, char.nick))

                    cmd = await read_command(ws)

                    if cmd["type"] == "create":
                        await create_character(ws, user, cmd["content"])
                    elif cmd["type"] == "choose":
                        return await choose_character(ws, user, cmd["content"])
                    else:
                        raise ClientEx("Invalid command")

            else:
                await prn(ws, "Create a character with \"/create <name> <nick>\": ")
                cmd = await read_command(ws)
                if cmd["type"] == "create":
                    await create_character(ws, user, cmd["content"])
                else:
                    raise ClientEx("Invalid command")

        except ClientEx as e:
            await prn(ws, str(e))