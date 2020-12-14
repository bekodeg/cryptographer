import text
import random
import math
text = text.Text()


def order(a, s):
    n = 1
    for _ in range(s):
        n = (n * a) % 1000_000_000_000
    return n


class Cipher:
    def __init__(self):
        self.info = ''

    def encryption_fun(self, *args):
        pass

    def decryption_fun(self, *args):
        pass

    def key_check(self, key, size):
        pass

    def key_generator(self, *args, **kwargs):
        pass

    def __str__(self):
        return self.info


class Caesar(Cipher):
    def __init__(self):
        super().__init__()
        self.info = 'Один из древнейших шифров алгоритмом является сдвиг всех символов'\
                    ' в право по алфавиту ключ - вличина сдвига'

    def encryption_fun(self, arr, size, key=(3, )):
        res = []
        for i in range(len(arr)):
            res.append((arr[i] + key[i % len(key)]) % size)
        return res

    def decryption_fun(self, arr, size, key=(3, )):
        res = []
        for i in range(len(arr)):
            res.append((arr[i] - key[i % len(key)]) % size)
        return res

    def key_check(self, key, size):
        res = []
        for i in key:
            d = ''
            for j in range(len(i)):
                if i[j].isdigit():
                    d += i[j]
                else:
                    if d:
                        r = int(d) % 256
                        res.append(r)
                    r = ord(i[j])
                    res.append(r)
            if d:
                r = int(d) % 256
                res.append(r)
        return True, res

    def key_generator(self, size=8, **kwargs):
        n = random.randint(1, size)
        res = []
        for _ in range(n):
            res.append(random.randint(1, size - 1))
        return ''.join(list(map(str, res)))


class MonoCipher(Cipher):
    def __init__(self):
        super().__init__()
        self.info = 'Шифр при котором каждому символу соответствует другой, ключ - алфавит'

    def encryption_fun(self, arr, size, key, **kwargs):
        res = []
        print('\n', arr, sep='')
        print(key)
        for i in arr:
            res.append(key[i])
        return res

    def decryption_fun(self, arr, size, key, **kwargs):
        res = []
        for i in arr:
            res.append(key.index(i % len(key)) % size)
        return res

    def key_check(self, key, size):
        print(len(set(key)), size)
        if len(set(key)) < size:
            return False,
        else:
            return True, text.to_string(key)[0]

    def key_generator(self, size=8, l_n=text.lib):
        res = list(l_n)
        random.shuffle(res)
        print(res)
        return ''.join(res)


class TranspositionCipher(Cipher):
    def __init__(self):
        super().__init__()
        self.info = 'шифр перестановки, ключ простое число'

    def encryption_fun(self, arr, size, key, beginning=0):
        print()
        print(key)
        res = []
        key = key[0]
        l_n = len(arr)
        for _ in range(l_n):
            beginning = (beginning + key) % l_n
            res.append(arr[beginning])
        return res

    def decryption_fun(self, arr, size, key, beginning=0):
        l_n = len(arr)
        res = [0] * l_n
        key = key[0]
        for i in arr:
            beginning = (beginning + key) % l_n
            res[beginning] = i
        return res

    def key_check(self, key, size):
        if type(key) == int:
            pass
        elif not key.isdigit():
            res = 0
            key = text.to_string(key)[0]
            r = text.l_l()
            for i in range(len(key)):
                res += (key[-i - 1] * order(r, i))
            key = res
        else:
            key = int(key)
        if size % key == 0:
            return self.key_check(key + 1, size)
        for i in range(2, int(key ** 0.5) + 1):
            if key % i == 0:
                return self.key_check(key + 1, size)
        return True, [key]

    def key_generator(self, size, **kwargs):
        res = random.randint(int(size ** 0.33), size ** 3)
        return str(res)