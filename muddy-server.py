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

from service.room import room_service

from controller.auth import auth_interface
from controller.character import manage_character

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


        # Administration
        if data["type"] == "ban":    # Ban a user
            pass
        if data["type"] == "priv":    # Change user privilege
            pass
        if data["type"] == "chown":   # Change owner of an object/room/script
            pass
        if data["type"] == "chmod":   # Change perms of an object/room/script
            pass


        # Room
        if data["type"] == "room_create": # Create a room
            pass
        if data["type"] == "room_link":   # Link a room to another one
            pass
        if data["type"] == "room_del":    # Delete a room
            pass


        # Actions
        if data["type"] == "drop":      # Drop something in the room
            pass
        if data["type"] == "take":      # Take something from the room
            pass
        if data["type"] == "give":      # Give something to someone
            pass
        if data["type"] == "whisper":   # Say something in private
            pass
        if data["type"] == "move":      # Move player to another room
            pass
        if data["type"] == "inventory": # Inspect inventory
            pass
        if data["type"] == "save":      # Save my character
            pass
        if data["type"] == "exit":      # Exit the server
            break
        if data["type"] == "say":       # Say something in public
            await prn(ws, user.name + " just said: " + str(data["content"]))


        # Script
        if data["type"] == "script_copy":    # Copy script
            pass
        if data["type"] == "script_detach":  # detach script from obj/room/char
            pass
        if data["type"] == "script_attach":  # attach script to obj/room/char
            pass
        if data["type"] == "script_destroy": # destroy obj/room/char/script
            pass
        if data["type"] == "script_rename":  # destroy obj/room/char/script
            pass
        if data["type"] == "script_upload":  # Create or update a script
            data = base64.b64decode(content["data"])
            name = content["name"]
            try:
                script_service.create_or_update(name, data)
            except ClientEx as e:
                await prn(ws, str(e))


init_data()

start_server = websockets.serve(main, args["<host>"], args["<port>"])

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

