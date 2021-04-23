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

async def choose_character(ws, user):
    while True:
        if len(user.characters) != 0:
            await prn(ws, "Please choose your character, or create one with \"/create <name> <nick>\": ")
            for char in user.characters:
                await prn(ws, "\t- {}: {}".format(char.name, char.nick))

        else:
            await prn(ws, "Create a character with \"/create <name>\": ")

            await create_characte(ws, )

async def create_character(ws, content):
    if len(content) != 5: raise ClientEx("Invalid arguments: /login <name> \"<email>\" <nick> \"<pass>\" \"<pass confirmation>\"")

    if content[3] != content[4]:
        raise ClientEx("Password does not match.")

    return user_repository.create_user(content[0], content[1], content[2], content[3])


async def main(ws, path):
    global world, players

    user = await auth_page(ws)
    character = await choose_character(ws, user)

    while True:
        loc = world.get_object(player.location)
        loc.load(player)

        loc.draw(player)

        data = await read_command(ws)

        if data["type"] == "cmd":
            cmd = data["content"]

            if not len(cmd):
                continue

            player.action = cmd
            loc.update(player)
            
        if data["type"] == "exit":
            break


if __name__ == '__main__':
    args = docopt(__doc__, version='0.1')

    world = ObjFile(args["<file>"])
    players = {
    }

    if args["--migrate"]: migrate()

    start_server = websockets.serve(main, args["<host>"], args["<port>"])

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

