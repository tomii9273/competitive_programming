# BinaryTrieBit でそこまで速くならなそうなので、基本的に BinaryTrie を使う。


class BinaryTrie:
    """二分トライ木。ノードは入れ子にせず配列 (list) で持つ (入れ子にすると多重 list となり、特に Python だと重そう)。"""

    def __init__(self, bit_depth: int):
        """bit_depth: 使用するビット数"""
        self.tree = [[0, 0, 0]]  # 中身は [0-child, 1-child, count] (child が 0 であるのは None の意味)
        self.bit_start = 1 << (bit_depth - 1)

    def add(self, x: int, n: int = 1) -> None:
        """x を n 個追加"""
        assert x >= 0
        assert n >= 0
        now = 0
        b = self.bit_start
        while b:
            self.tree[now][2] += n
            i = bool(x & b)
            if self.tree[now][i] == 0:
                self.tree.append([0, 0, 0])
                self.tree[now][i] = len(self.tree) - 1
            now = self.tree[now][i]
            b >>= 1
        self.tree[now][2] += n

    def one(self, x: int) -> int:
        """x を 1 個追加、すでに 1 個以上ある場合は何もしない。最終的な x の個数を返す"""
        assert x >= 0
        now = 0
        b = self.bit_start
        nodes = []
        while b:
            nodes.append(now)
            i = bool(x & b)
            if self.tree[now][i] == 0:
                self.tree.append([0, 0, 0])
                self.tree[now][i] = len(self.tree) - 1
            now = self.tree[now][i]
            b >>= 1
        nodes.append(now)
        if self.tree[now][2] == 0:
            for ind in nodes:
                self.tree[ind][2] += 1
        return self.tree[now][2]

    def count(self, x: int) -> int:
        """x の個数を返す"""
        assert x >= 0
        now = 0
        if self.tree[now][2] == 0:
            return 0
        b = self.bit_start
        while b:
            i = bool(x & b)
            if self.tree[now][i] == 0:
                return 0
            now = self.tree[now][i]
            b >>= 1
        return self.tree[now][2]

    def remove(self, x: int, n: int = 1) -> int:
        """x を n 個を上限にできるだけ削除、削除できた数を返す"""
        assert x >= 0
        assert n >= 0
        now = 0
        b = self.bit_start
        nodes = []
        while b:
            nodes.append(now)
            i = bool(x & b)
            if self.tree[now][i] == 0:
                nodes = []
                break
            now = self.tree[now][i]
            b >>= 1
        if len(nodes) == 0 or now == 0:
            return 0
        nodes.append(now)
        ans = min(self.tree[now][2], n)
        for ind in nodes:
            self.tree[ind][2] -= ans
        return ans

    def get_min_xor(self, x: int) -> int:
        """i xor x が最小となる要素 i を (空なら -1 を) 取得 (i xor x を返すわけではないので注意)"""
        assert x >= 0
        now = 0
        if self.tree[now][2] == 0:
            return -1
        b = self.bit_start
        ans = 0
        while b:
            assert self.tree[now][2] > 0
            i = bool(x & b)
            if self.tree[now][i] == 0 or self.tree[self.tree[now][i]][2] == 0:
                i ^= 1
            ans ^= i * b
            now = self.tree[now][i]
            b >>= 1
        assert self.tree[now][2] > 0
        return ans


class BinaryTrieBit:
    """
    二分トライ木。ノードは配列 (list) にビットで持つ。
    [0-child, 1-child, count] と list で持つより速いはずだが、そこまで速くなっていなそう。
    """

    def __init__(self, bit_depth: int):
        """bit_depth: 使用するビット数"""
        # 中身は、下から 30 ビットが 0-child、その上の 30 ビットが 1-child、その上が count (child が 0 であるのは None の意味)
        self.tree = [0]
        self.bit_start = 1 << (bit_depth - 1)
        self.mask = (1 << 30) - 1

    def add(self, x: int, n: int = 1) -> None:
        """x を n 個追加"""
        assert x >= 0
        assert n >= 0
        now = 0
        b = self.bit_start
        while b:
            self.tree[now] += n << 60
            i = bool(x & b)
            if (self.tree[now] >> (30 * i)) & self.mask == 0:
                self.tree.append(0)
                if i:
                    self.tree[now] = (
                        (self.tree[now] >> 60 << 60) | ((len(self.tree) - 1) << 30) | (self.tree[now] & self.mask)
                    )
                else:
                    self.tree[now] = (self.tree[now] >> 30 << 30) | (len(self.tree) - 1)
            now = (self.tree[now] >> (30 * i)) & self.mask
            b >>= 1
        self.tree[now] += n << 60

    def one(self, x: int) -> int:
        """x を 1 個追加、すでに 1 個以上ある場合は何もしない。最終的な x の個数を返す"""
        assert x >= 0
        now = 0
        b = self.bit_start
        nodes = []
        while b:
            nodes.append(now)
            i = bool(x & b)
            if (self.tree[now] >> (30 * i)) & self.mask == 0:
                self.tree.append(0)
                if i:
                    self.tree[now] = (
                        (self.tree[now] >> 60 << 60) | ((len(self.tree) - 1) << 30) | (self.tree[now] & self.mask)
                    )
                else:
                    self.tree[now] = (self.tree[now] >> 30 << 30) | (len(self.tree) - 1)
            now = (self.tree[now] >> (30 * i)) & self.mask
            b >>= 1
        nodes.append(now)
        if self.tree[now] >> 60 == 0:
            for ind in nodes:
                self.tree[ind] += 1 << 60
        return self.tree[now] >> 60

    def count(self, x: int) -> int:
        """x の個数を返す"""
        assert x >= 0
        now = 0
        if self.tree[now] >> 60 == 0:
            return 0
        b = self.bit_start
        while b:
            i = bool(x & b)
            if (self.tree[now] >> (30 * i)) & self.mask == 0:
                return 0
            now = (self.tree[now] >> (30 * i)) & self.mask
            b >>= 1
        return self.tree[now] >> 60

    def remove(self, x: int, n: int = 1) -> int:
        """x を n 個を上限にできるだけ削除、削除できた数を返す"""
        assert x >= 0
        assert n >= 0
        now = 0
        b = self.bit_start
        nodes = []
        while b:
            nodes.append(now)
            i = bool(x & b)
            if self.tree[now] >> (30 * i) & self.mask == 0:
                nodes = []
                break
            now = (self.tree[now] >> (30 * i)) & self.mask
            b >>= 1
        if len(nodes) == 0 or now == 0:
            return 0
        nodes.append(now)
        ans = min(self.tree[now] >> 60, n)
        for ind in nodes:
            self.tree[ind] -= ans << 60
        return ans

    def get_min_xor(self, x: int) -> int:
        """i xor x が最小となる要素 i を (空なら -1 を) 取得 (i xor x を返すわけではないので注意)"""
        assert x >= 0
        now = 0
        if (self.tree[now] >> 60) == 0:
            return -1
        b = self.bit_start
        ans = 0
        while b:
            i = bool(x & b)
            if (self.tree[now] >> (30 * i)) & self.mask == 0 or self.tree[
                (self.tree[now] >> (30 * i)) & self.mask
            ] >> 60 == 0:
                i ^= 1
            ans ^= i * b
            now = (self.tree[now] >> (30 * i)) & self.mask
            b >>= 1
        return ans
