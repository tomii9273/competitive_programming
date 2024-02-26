from random import randint


class ProtectedDict(dict):
    """
    キーにランダムな値を足してから辞書に追加することで、キーのハッシュ衝突攻撃を防ぐ辞書クラス。
    参考: https://codeforces.com/blog/entry/101817
    """

    def __init__(self):
        self.salt = randint(1, 10**8)
        super().__init__()

    def __setitem__(self, key, value):
        super().__setitem__(key + self.salt, value)

    def __getitem__(self, key):
        return super().__getitem__(key + self.salt)

    def __delitem__(self, key):
        super().__delitem__(key + self.salt)

    def __contains__(self, key):
        return super().__contains__(key + self.salt)

    def keys(self) -> set:
        return set(key - self.salt for key in super().keys())

    def values(self) -> set:
        return set(super().values())

    def items(self) -> set:
        return set((key - self.salt, value) for key, value in super().items())
