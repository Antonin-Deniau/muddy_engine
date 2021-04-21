#!/usr/bin/env python
import asyncio
import sys
import atexit
import json
import os
import traceback
import shlex
from pyreadline import Readline
readline = Readline()


from core import ObjFile


histfile = os.path.join(os.path.expanduser("~"), ".game_history")
try:
    readline.read_history_file(histfile)
    h_len = readline.get_current_history_length()
except FileNotFoundError:
    open(histfile, 'wb').close()
    h_len = 0

def save(prev_h_len, histfile):
    new_h_len = readline.get_current_history_length()
    readline.set_history_length(1000)
    #readline.append_history_file(new_h_len - prev_h_len, histfile)
atexit.register(save, h_len, histfile)


async def repl():
    world = ObjFile(sys.argv[1])

    player_name = "antonin"

    players = {
            "antonin": world.get_class("player")(world, "antonin"),
    }

    while True:
        player = players[player_name]

        loc = world.get_object(player.location)
        loc.load(player)

        loc.draw(player)

        cmd = list(shlex.shlex(input(">")))
        if not len(cmd):
            continue

        if cmd[0] == "exit":
            break

        player.action = cmd
        loc.update(player)

    return True

async def main():
    await repl()

asyncio.run(main())

