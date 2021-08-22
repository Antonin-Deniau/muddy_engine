from cmud.core import ns
from cmud.parser_t import parse
from cmud.eval_core import evl
from cmud.environment import Env

def read(e):
    return parse(e)

def exec(e, env):
    b = read(e)
    c = evl(b, env)
    return c

def create_blank_env():
    repl_env = Env(None, [], [])
    for k, v in ns.items():
        repl_env.set(k, v)
    return repl_env

def load_str(e, env):
    b = read(e)
    evl(b, env)
