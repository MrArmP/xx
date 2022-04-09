from re import findall
def get_config():
    with open("config.txt", "r") as r:
        read = r.read()
    pattern = r"(.*)="
    res = {}
    reg = findall(pattern, read)
    for char in reg:
        ok = findall(f'{char}=(.*)', read)[0]
        res[char] = ok
    return res
try:
    from munch import Munch
except ImportError:
    from os import system; system("python3 -m pip install munch")
def get(d= get_config()):
    for i in d:
        if isinstance(d[i], dict):
            d[i] = get(d[i])
    return Munch(d)