#!/usr/bin/env python
import asyncio
import sys
import atexit
import json
import os
import readline
import traceback
import shlex

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
    readline.append_history_file(new_h_len - prev_h_len, histfile)
atexit.register(save, h_len, histfile)



world = ObjFile(sys.argv[1])

gamestate = {
    "previous_location": None,
    "location": world.get_metadata("entrypoint"),
    "world": world,
}


players = {
        "antonin": gamestate,
}

async def repl():
    global players
    player_name = "antonin"

    while True:
        loc = world.get_object(players[player_name]["location"])


        loc.draw(gamestate)

        cmd = list(shlex.shlex(input(">")))
        if not len(cmd):
            continue

        if cmd[0] == "exit":
            break

        players[player_name]["action"] = cmd
        players[player_name] = loc.update(players[player_name])

    return True

async def main():
    await repl()

asyncio.run(main())

