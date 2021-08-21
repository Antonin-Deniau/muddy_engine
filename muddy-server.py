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

def init_data():
    room_service.init()

async def main(ws, path):
    user = await auth_interface(ws)
    character = await manage_character(ws, user)

    action = None
    while True:
        await character.room.exec(ws, character)

        data = await read_command(ws)

        # object perms: inspect/modify
        # room perms:   visit/modify
        # script perms: inspect/modify
        # owners: UGO

        if data["type"] == "say":     # Say something in public
            await prn(ws, user.name + " just said: " + str(data["content"]))

        # TO IMPLEMENT
        if data["type"] == "ban":    # Ban a user
            pass
        if data["type"] == "priv":    # Change user privilege
            pass
        if data["type"] == "deletegrp": # Delete a group
            pass
        if data["type"] == "listgrp": # List groups
            pass
        if data["type"] == "creategrp": # Create a group
            pass
        if data["type"] == "grprm":   # Remove user from group
            pass
        if data["type"] == "grpadd":  # Add user to group
            pass
        if data["type"] == "chown":   # Change owner of an object/room/script
            pass
        if data["type"] == "chmod":   # Change perms of an object/room/script
            pass
        if data["type"] == "dig":     # Create a room
            pass
        if data["type"] == "link":    # Link a room to another one
            pass
        if data["type"] == "drop":    # Drop something in the room
            pass
        if data["type"] == "take":    # Take something from the room
            pass
        if data["type"] == "give":    # Give something to someone
            pass
        if data["type"] == "whisper": # Say something in private
            pass
        if data["type"] == "move":    # Move player to another room
            pass
        if data["type"] == "copy":    # Copy script
            pass
        if data["type"] == "detach":  # detach script from obj/room/exit
            pass
        if data["type"] == "attach":  # attach script to obj/room/exit
            pass
        if data["type"] == "upload":  # Create or update a script
            pass
        if data["type"] == "save":    # Save my character
            pass


        if data["type"] == "exit":    # Exit the server
            break

init_data()

start_server = websockets.serve(main, args["<host>"], args["<port>"])

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

