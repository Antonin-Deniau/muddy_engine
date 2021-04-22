import json
from exceptions import ClientEx, ExitEx


async def send_command(ws, t, content):
    await ws.send(json.dumps({ "content": content, "type": t }))

async def read_command(ws):
    return json.loads(await ws.recv())

async def prn(ws, data):
    await send_command(ws, "prn", data)

async def get_word(ws):
    while True:
        data = await read_command(ws)

        try: 
            if data["type"] != "cmd":
                if data["type"] == "exit":
                    raise ExitEx

                raise ClientEx("Invalid command type")

            if len(data["content"]) == 0:
                raise ClientEx("You must enter some text")

            return data["content"][0]
        except ClientEx as e:
            await prn(ws, str(e))

