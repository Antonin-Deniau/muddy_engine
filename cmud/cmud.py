from core import ns
from parser_t import parse
from eval_core import evl
from environment import Env

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
