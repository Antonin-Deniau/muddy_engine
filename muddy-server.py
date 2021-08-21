#!/usr/bin/env python
"""Server for the Muddy MUD framework
Usage:
  muddy-server [--migrate] <host> <port> <world_folder>
  muddy-server -h | --help
  muddy-server --version
Options:
  -h --help       Show this help
  --version       Show the program version
  <host>          The host of the server
  <port>          The port of the server
  <world_folder>  The world folder for the game
"""
from docopt import docopt
import asyncio
import websockets

from core.utils import read_command
from core.persist import migrate

from service.room import room_service

from controller.auth import auth_interface
from controller.character import manage_character

args = docopt(__doc__, version='0.1')

if args["--migrate"]: migrate()

def init_data():
    room_service.init()

async def main(ws, path):
    user = await auth_interface(ws)
    character = await manage_character(ws, user)

    while True:
        await character.room.exec(ws, character)

        data = await read_command(ws)

        if data["type"] == "cmd":
            cmd = data["content"]

            if not len(cmd):
                continue

            character.set_action(cmd)
            await loc.update(ws, character)

        if data["type"] == "exit":
            break

start_server = websockets.serve(main, args["<host>"], args["<port>"])

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

