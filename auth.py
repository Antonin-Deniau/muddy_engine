from utils import send_command, read_command, prn
from user import user_repository


async def auth_page(ws):
    await prn(ws, "Welcome to [Themud], to login type \"/login <name> <pass>\" To register \"/register\"")

    while True:
        cmd = await read_command(ws)

        try:
            if cmd["type"] == "login":
                return await login(ws, cmd["content"])
            elif cmd["type"] == "register":
                return await register(ws, cmd["content"])
            else:
                raise Exception("Invalid command")

        except Exception as e:
            await prn(ws, str(e))


async def login(ws, content):
    if len(content) != 2: raise Exception("Invalid arguments: /login <name> <pass>")

    user = user_repository.fetch_user(content[0])
    if user:
        if not user.verify_password(content[1]):
            raise Exception("Invalid username or password.")

        return user
    else:
        raise Exception("Invalid username or password.")


async def register(ws, content):
    raise Exception("Not implemented")
