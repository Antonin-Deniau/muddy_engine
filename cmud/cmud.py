from cmud.core import ns
from cmud.parser_t import parse
from cmud.eval_core import evl
from cmud.environment import Env

def read(e):
    return parse(e)

async def exec(e, env):
    b = read(e)
    c = await evl(b, env)
    return c

def create_blank_env():
    repl_env = Env(None, [], [])
    for k, v in ns.items():
        repl_env.set(k, v)
    return repl_env

async def load_str(e, env):
    b = read(e)
    await evl(b, env)
