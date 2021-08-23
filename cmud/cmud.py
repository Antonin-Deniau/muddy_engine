import types, asyncio
from cmud.core import ns
from cmud.parser_t import parse
from cmud.eval_core import evl
from cmud.environment import Env
from cmud.basl_types import Fn

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


async def run_basl_fnc(f, args):
    if isinstance(f, Fn):
        ast, env = f.ast, Env(f.env, f.params, args, "<<START SCRIPT>>")
        return await evl(ast, env)

    if isinstance(f, types.LambdaType):
        if asyncio.iscoroutinefunction(f):
            return await f(*args)
        else:
            return f(*args)
