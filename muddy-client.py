#!/usr/bin/env python
"""Connect to a Muddy powered mud server
Usage:
  muddy-client cli [--frame=<frame>] <url>
  muddy-client -h | --help
  muddy-client --version
Options:
  -h --help        Show this help
  --version        Show the program version
  <url>            Url to connect to
  --frame=<frame>  The frame to attach to [default: all]
"""
from docopt import docopt
import asyncio
from pathlib import Path
import websockets
import shlex
import os
import base64
import re

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from core.utils import send_command, read_command

home = Path.home()
histfile = os.path.abspath(os.path.join(Path.home(), '.muddy_history'))


slash_regex = re.compile(r"\\(.)", re.IGNORECASE)
command_regex = re.compile(r'(?:(?:(?:[^ "\\]|\\.)+)|"(?:[^\\"]|\\.)+")', re.IGNORECASE)

def split_command(data):
    word_list = re.findall(command_regex, data)
    return [slash_regex.sub(r"\1", word) for word in word_list]

async def upload_script(ws, cmd):
    if len(cmd) != 2: return print("Invalid arguments: /upload <id> <filepath>")

    cwd = os.getcwd()

    fpath = os.path.join(cwd, cmd[1])

    if os.path.exists(fpath) and os.path.isfile(fpath):
        f = open(fpath, "rb")
        content = base64.b64encode(f.read())

        await send_command(ws, "set", ["script", cmd[0], "code", content.decode("utf-8")])
    else:
        print("File does not exist")


async def send_inputs(ws):
    session = PromptSession(history=FileHistory(histfile))

    while True:
        with patch_stdout():
            raw = await session.prompt_async(">", auto_suggest=AutoSuggestFromHistory())

        if len(raw) == 0:
            continue

        if raw[0] == "/":
            rm_slash = split_command(raw[1:])

            t = rm_slash[0]
            cmd = rm_slash[1:]

            if t == "upload":
                await upload_script(ws, cmd)
            else:
                await send_command(ws, t, cmd)
        else:
            await send_command(ws, "say", raw)

async def main():
    args = docopt(__doc__, version='0.1')

    hist = Path(histfile)
    hist.touch(exist_ok=True)

    async with websockets.connect(args["<url>"]) as ws:
        asyncio.ensure_future(send_inputs(ws))

        while True:
            data = await read_command(ws)

            if data["type"] == "exit":
                break

            if data["type"] == "prn":
                if args["--frame"] == "all" or args["--frame"] == data["frame"]:
                    print(data["content"])

        return True

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
