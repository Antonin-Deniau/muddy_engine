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

from core.utils import read_command, prn
from core.persist import migrate
from core.exceptions import ClientEx

from service.room import room_service

from controller.auth import auth_interface
from controller.character import manage_character
from controller.actions import actions
from controller.build import build
from controller.room import room
from controller.script import script
from controller.admin import admin

args = docopt(__doc__, version='0.1')

if args["--migrate"]: migrate()

banner = "Welcome to Muddy Engine!"

# Init fixtures
def init_data():
    room_service.init()

async def main(ws, path):
    await prn(ws, banner)

    user = await auth_interface(ws)
    character = await manage_character(ws, user)

    action = None
    while True:
        await character.room.exec(ws, character)

        data = await read_command(ws)

        if data["type"] == "exit": # Exit the server
            break
        
        try:
            await admin(ws, user, data)
            await build(ws, user, data)
            await room(ws, user, data)
            await actions(ws, user, data)
            await script(ws, user, data)

        except ClientEx as e:
            await prn(ws, str(e))


init_data()

start_server = websockets.serve(main, args["<host>"], args["<port>"])

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

