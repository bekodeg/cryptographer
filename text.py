class Text():
    def __init__(self):
        with open('library.txt', mode='rt', encoding='utf8') as f:
            self.lib = f.read()
            self.l_n = len(set(self.lib))

    def l_l(self):
        return self.l_n

    def to_string(self, arr):
        res = [[], '']
        for i in arr:
            if type(i) == str and i in self.lib:
                res[0].append(self.lib.index(i))
            elif type(i) == int:
                res[1] += self.lib[i]
        return res
