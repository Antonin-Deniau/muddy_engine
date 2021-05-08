#!/usr/bin/env python
"""Server for the Muddy MUD framework
Usage:
  muddy-server [--migrate] <host> <port> <file>
  muddy-server -h | --help
  muddy-server --version
Options:
  -h --help  Show this help
  --version  Show the program version
  <host>     The host of the server
  <port>     The port of the server
  <file>     The main file of the game
"""
from docopt import docopt
import asyncio
import websockets
from utils import send_command, read_command, prn
from auth import auth_page
from core import ObjFile
from persist import migrate
from exceptions import ClientEx
from character import character_repository
from user import user_repository


async def create_character(ws, user, content):
    if len(content) != 2: raise ClientEx("Invalid arguments: /create <name> <nick>")
    return character_repository.create_character(content[0], content[1], user, "", "")

async def choose_character(ws, content):
    pass

async def manage_character(ws, user):
    while True:
        #user_repository.session.refresh(user)

        try:
            if len(user.characters) != 0:
                await prn(ws, "Please choose your character with \"/choose <name>\", or create one with \"/create <name> <nick>\": ")
                for char in user.characters:
                    await prn(ws, "\t- {}: {}".format(char.name, char.nick))

                    cmd = await read_command(ws)

                    if cmd["type"] == "create":
                        await create_character(ws, user, cmd["content"])
                    elif cmd["type"] == "choose":
                        return await choose_character(ws, cmd["content"])
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


args = docopt(__doc__, version='0.1')

world = ObjFile(args["<file>"])
if args["--migrate"]: migrate()

async def main(ws, path):
    global world

    user = await auth_page(ws)
    character = await manage_character(ws, user)

    while True:
        loc = world.get_object(character.location)
        loc.load(character)

        loc.draw(character)

        data = await read_command(ws)

        if data["type"] == "cmd":
            cmd = data["content"]

            if not len(cmd):
                continue

            character.set_action(cmd)
            loc.update(character)

        if data["type"] == "exit":
            break

start_server = websockets.serve(main, args["<host>"], args["<port>"])

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

