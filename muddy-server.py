#!/usr/bin/env python
"""Server for the Muddy MUD framework
Usage:
  muddy-server [--migrate] <host> <port>
  muddy-server -h | --help
  muddy-server --version
Options:
  -h --help       Show this help
  --version       Show the program version
  <host>          The host of the server
  <port>          The port of the server
"""
from dotenv import load_dotenv
load_dotenv()

from docopt import docopt
import asyncio
import websockets

from core.utils import read_command, prn
from core.persist import migrate
from core.exceptions import ClientEx

from service.room import room_service
from service.ws_conn import ws_conn

# Auth phase
from controller.auth import auth_interface
from controller.character import manage_character

# Commands
from controller.actions import actions
from controller.build import build
from controller.script import script
from controller.admin import admin

args = docopt(__doc__, version='0.1')

if args["--migrate"]:
    migrate()
    room_service.init()

banner = "Welcome to Muddy Engine!"

async def main(ws, path):
    await prn(ws, banner)

    user = await auth_interface(ws)
    char = await manage_character(ws, user)
    ws_conn.add(char, ws)

    try:
        char.room.characters.add(char)
        await room_service.look_user_room(ws, char)
        await room_service.send_message(char.room, "{} walked in.".format(char.name), [char.id])

        action = None
        while True:
            data = await read_command(ws)

            if data["type"] == "exit": # Exit the server
                break
            
            try:
                await admin(ws, char, data)
                await build(ws, char, data)
                await actions(ws, char, data)
                await script(ws, char, data)

            except ClientEx as e:
                await prn(ws, str(e))
    finally:
        ws_conn.remove(char)
        char.room.characters.remove(char)
        await room_service.send_message(char.room, "{} disapeared.".format(char.name), [char.id])


start_server = websockets.serve(main, args["<host>"], args["<port>"])

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

