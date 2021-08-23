from functools import reduce
import types, traceback, asyncio

from cmud.basl_types import Fn, Name, BaslException, Keyword, Atom
from cmud.parser_t import display
from cmud.environment import Env


### SYMBOLS ###

def quasiquote_process_list(ast):
    res = tuple([])
    for elt in reversed(ast):
        if isinstance(elt, tuple) and len(elt) != 0 and isinstance(elt[0], Name) and elt[0].name == "splice-unquote":
            res = tuple([Name("concat"), elt[1], res])
        else:
            res = tuple([Name("cons"), quasiquote(elt), res])

    return res

def quasiquote(ast):
    if isinstance(ast, tuple):
        if len(ast) != 0 and isinstance(ast[0], Name):
            if isinstance(ast[0], Name) and ast[0].name == "unquote":
                return ast[1]
        return quasiquote_process_list(ast)

    if isinstance(ast, list):
        return tuple([Name("vec"), quasiquote_process_list(tuple(ast))])

    if isinstance(ast, dict) or isinstance(ast, Name):
        return tuple([Name("quote"), ast])

    return ast

def is_macro_call(ast, env):
    if isinstance(ast, tuple) and isinstance(ast[0], Name):
        try:
            return env.get(ast[0].name).is_macro
        except:
            return False
    else:
        return False

def macroexpand(ast, env):
    while is_macro_call(ast, env):
        fnc = env.get(ast[0].name)
        ast = fnc.fn(*ast[1:])

    return ast

### EVAL PART ###

async def evl(ast, env):
    while True:
        if isinstance(ast, tuple):
            if len(ast) == 0: return  ast

            ast = macroexpand(ast, env)
            if not isinstance(ast, tuple): return await eval_ast(ast, env)

            if isinstance(ast[0], Keyword):
                hm = await evl(ast[1], env)
                return hm[ast[0].name]

            if isinstance(ast[0], Name):
                if ast[0].name == "def!":
                    value = await evl(ast[2], env)
                    return env.set(ast[1].name, value)

                if ast[0].name == "defmacro!":
                    value = await evl(ast[2], env)
                    value.is_macro = True
                    return env.set(ast[1].name, value)

                if ast[0].name == "let*":
                    new_env = Env(env, [], [])
                    binding_list = ast[1]

                    for i in zip(binding_list[::2], binding_list[1::2]):
                        data = await evl(i[1], new_env)
                        new_env.set(i[0], data)

                    ast, env = ast[2], new_env; continue

                if ast[0].name == "try*":
                    if len(ast) < 3:
                        return await evl(ast[1], env)

                    try:
                        return await evl(ast[1], env)
                    except BaslException as e:
                        new_env = Env(env, [ast[2][1].name], [e])
                        return await evl(ast[2][2], new_env)
                    except Exception as e:
                        new_env = Env(env, [ast[2][1].name], [str(e)])
                        return await evl(ast[2][2], new_env)

                if ast[0].name == "raise":
                    s = "{}:{}".format(ast[0].name, ast[0].line) if isinstance(ast[0], Name) else "LAMBDA<" + ast[0] + ">"
                    raise BaslException(await evl(ast[1], env), [*env.stack, s])

                if ast[0].name == "quote":
                    return ast[1]

                if ast[0].name == "macroexpand":
                    return macroexpand(ast[1], env)

                if ast[0].name == "quasiquoteexpand":
                    return quasiquote(ast[1])

                if ast[0].name == "quasiquote":
                    ast = quasiquote(ast[1]); continue

                if ast[0].name == "do":
                    res = None
                    for x in ast[1:-1]:
                        res = await evl(x, env)
                    ast = ast[-1]; continue

                if ast[0].name == "if":
                    if len(ast) < 3: ast, env = None, env; continue
                    res_cond = await evl(ast[1], env)

                    if type(res_cond) == bool and res_cond == True: ast = ast[2]; continue
                    if type(res_cond) == int: ast = ast[2]; continue
                    if type(res_cond) == float: ast = ast[2]; continue
                    if type(res_cond) == list: ast = ast[2]; continue
                    if type(res_cond) == tuple: ast = ast[2]; continue
                    if type(res_cond) == str: ast = ast[2]; continue
                    if type(res_cond) == Fn: ast = ast[2]; continue
                    if type(res_cond) == Keyword: ast = ast[2]; continue
                    if type(res_cond) == Name: ast = ast[2]; continue
                    if type(res_cond) == types.LambdaType: ast = ast[2]; continue
                    if type(res_cond) == Atom: ast = ast[2]; continue

                    ast = ast[3] if len(ast) >= 4 else None; continue

                if ast[0].name == "fn*":
                    body = ast[2]
                    params = ast[1]

                    async def func(*e):
                        return await evl(body, Env(env, params, e))

                    return Fn(body, params, env, func)

            [f, *args] = await eval_ast(ast, env)

            if isinstance(f, Fn):
                s = "{}:{}:{}".format(ast[0].name, ast[0].line) if isinstance(ast[0], Name) else "LAMBDA<" + display(ast[0], True) + ">"
                ast, env = f.ast, Env(f.env, f.params, args, s)
                continue

            if isinstance(f, types.LambdaType):
                print(f, args)
                return f(*args)

        return await eval_ast(ast, env)

async def eval_ast(ast, env):
    if isinstance(ast, dict):
        return { k: await evl(v, env) for k,v in ast.items() }

    if isinstance(ast, Name):
        return env.get(ast.name)

    if isinstance(ast, list):
        return list([await evl(a, env) for a in ast])

    if isinstance(ast, tuple):
        return tuple([await evl(x, env) for x in ast])

    return ast
