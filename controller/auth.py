from .core.utils import read_command, prn
from .service.user import user_service

from exceptions import ClientEx

async def auth_interface(ws):
    await prn(ws, "Welcome to [Themud], to login type \"/login <name> <pass>\" To register \"/register\"")

    while True:
        cmd = await read_command(ws)

        try:
            if cmd["type"] == "login":
                return await login(ws, cmd["content"])
            elif cmd["type"] == "register":
                return await register(ws, cmd["content"])
            else:
                raise ClientEx("Invalid command")

        except ClientEx as e:
            await prn(ws, str(e))


async def login(ws, content):
    if len(content) != 2: raise ClientEx("Invalid arguments: /login <name> <pass>")

    user = user_service.fetch_user(content[0])
    if user:
        if not user.verify_password(content[1]):
            raise ClientEx("Invalid username or password.")

        return user
    else:
        raise ClientEx("Invalid username or password.")


async def register(ws, content):
    if len(content) != 5: raise ClientEx("Invalid arguments: /login <name> \"<email>\" <nick> \"<pass>\" \"<pass confirmation>\"")

    if content[3] != content[4]:
        raise ClientEx("Password does not match.")

    return user_service.create_user(content[0], content[1], content[2], content[3])
