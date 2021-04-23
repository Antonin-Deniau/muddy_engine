import json
from exceptions import ClientEx, ExitEx


async def send_command(ws, t, content):
    await ws.send(json.dumps({ "content": content, "type": t }))

async def read_command(ws):
    return json.loads(await ws.recv())

async def prn(ws, data):
    await send_command(ws, "prn", data)
