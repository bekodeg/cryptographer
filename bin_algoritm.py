def encoding(file):
    with open(file, mode='rb') as f:
        v = f.read()
        res = []
        for i in v:
            res.append(i)
        return res


def decoding(file, data):
    with open(file, mode='wb') as f:
        data = bytes(map(int, data.split()))
        f.write(data)


def bete_cut(b):
    if type(b) == str:
        b = int(b)
    res = []
    while b > 0:
        res.append(b % 2)
        b //= 2
    while len(res) < 8:
        res.append(0)
    reversed(res)
    return res[-8:]
