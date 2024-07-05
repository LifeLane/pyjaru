import builtins

def pyjaru_print(*args):
    builtins.print(*args)

def pyjaru_len(obj):
    return len(obj)

standard_library = {
    'print': pyjaru_print,
    'len': pyjaru_len,
}
