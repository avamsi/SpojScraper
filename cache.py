import os, json

try:
    os.mkdir('cache')
except OSError:
    pass

def dump(i, names, probs, users):
    with open('cache/i', 'wb') as ifp, open('cache/names', 'wb') as nfp,\
    open('cache/probs', 'wb') as pfp, open('cache/users', 'wb') as ufp:
        json.dump(i, ifp)
        json.dump(names, nfp)
        json.dump(probs, pfp)
        json.dump(users, ufp)

def load():
    with open('cache/names', 'rb') as nfp,\
    open('cache/probs', 'rb') as pfp, open('cache/users', 'rb') as ufp:
        names = json.load(nfp)
        probs = json.load(pfp)
        users = json.load(ufp)
    return names, probs, users

def load_prev():
    if os.path.isfile('cache/i'):
        with open('cache/i', 'rb') as ifp:
            prev = json.load(ifp)
    else:
        prev = -1
        dump(-1, {}, [], {})
    return prev
