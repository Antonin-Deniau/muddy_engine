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
from utils import send_command, read_command
from auth import auth_page
from core import ObjFile
from persist import migrate

async def main(ws, path):
    global world, players

    player = await auth_page(ws)

    if not logged_in:
        return

    player = players[player_name]
    #world.get_class("player")(world, "antonin")

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

