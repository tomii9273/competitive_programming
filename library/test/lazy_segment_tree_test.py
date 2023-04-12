import sys

# sys.setrecursionlimit(10 ** 9)  # Codeforcesでは350000程度に


def input():
    return sys.stdin.readline().strip()


n, q = map(int, input().split())
A = list(map(int, input().split()))
Q = [list(map(int, input().split())) for _ in range(q)]
mod = 998244353


def e():
    return 0
    # return (0, 0)


mask = (1 << 32) - 1
id_ = 1 << 32


def op(x0, x1):
    return (((x0 >> 32) + (x1 >> 32)) % mod << 32) + (x0 & mask) + (x1 & mask)
    # return ((x0[0] + x1[0]) % mod, x0[1] + x1[1])


def mapping(x, f):
    # print(f, x)
    return (((f >> 32) * (x >> 32) + (f & mask) * (x & mask)) % mod << 32) + (x & mask)
    # return ((f[0] * x[0] % mod + f[1] * x[1] % mod) % mod, x[1])


def composition(f0, f1):
    return ((f0 >> 32) * (f1 >> 32) % mod << 32) + ((f0 & mask) * (f1 >> 32) + (f1 & mask)) % mod
    # return ((f0[0] * f1[0]) % mod, (f0[1] * f1[0] % mod + f1[1]) % mod)


def id():
    return id_
    # return (1, 0)


class LazySegtree:
    """
    遅延評価セグメント木
    参考: https://algo-logic.info/segment-tree/
    """

    def __init__(self, n):
        # size は最初に定めたサイズ、size2 は 2 の累乗の値をとるサイズ (>=size)
        self.size = n
        i = 1
        size_log = 0
        while i < n:
            i *= 2
            size_log += 1
        self.e = e()
        self.id = id()
        self.tree = [self.e for _ in range(2 * i - 1)]
        self.lazy = [self.id for _ in range(2 * i - 1)]
        self.size2 = i
        self.size_log = size_log

    def __getitem__(self, i):
        """[i] で i 番目の値を得られる。O(log n)"""
        if i < 0:
            i %= self.size
        return self.prod(i, i + 1)

    def _eval(self, k):
        """(内部 index の) k について (遅延させていた) 評価を行う。O(1)"""
        lazy_k = self.lazy[k]
        if lazy_k == self.id:
            return
        if k < self.size2 - 1:
            self.lazy[2 * k + 1] = composition(self.lazy[2 * k + 1], lazy_k)
            self.lazy[2 * k + 2] = composition(self.lazy[2 * k + 2], lazy_k)
        self.tree[k] = mapping(self.tree[k], lazy_k)
        self.lazy[k] = self.id

    # def update(self, i, x):  # 旧 (バグがある方)
    #     """i 番目の値を x に更新。O(log n)"""
    #     j = self.size2 + i - 1
    #     self.tree[j] = x
    #     while j > 0:
    #         j = (j - 1) // 2
    #         self.tree[j] = op(self.tree[2 * j + 1], self.tree[2 * j + 2])

    def update(self, i, x):  # 新 (バグを直した方)
        """i 番目の値を x に更新。O(log n)"""
        # i 番目が含まれるノードについて、上から下まで、遅延させていた評価を完了させる
        j = self.size2 + i
        for i in range(self.size_log, -1, -1):
            self._eval((j >> i) - 1)
        # 一番下の更新
        j -= 1
        self.tree[j] = x
        # 下から上まで更新
        while j > 0:
            j = (j - 1) // 2
            self.tree[j] = op(self.tree[2 * j + 1], self.tree[2 * j + 2])

    def apply(self, a, b, x, k=0, ll=0, rr=None):
        """
        区間 [a, b) に x を作用させる。O(log n)
        k は今見ている内部 index の番号、[ll, rr) は self.tree[k] が表す区間。
        """
        if rr is None:
            rr = self.size2
        self._eval(k)
        if a <= ll and rr <= b:
            self.lazy[k] = composition(self.lazy[k], x)
            self._eval(k)
        elif a < rr and ll < b:  # [ll, rr) が [a, b) に含まれないが、共通部分はある場合
            self.apply(a, b, x, 2 * k + 1, ll, (ll + rr) // 2)
            self.apply(a, b, x, 2 * k + 2, (ll + rr) // 2, rr)
            self.tree[k] = op(self.tree[2 * k + 1], self.tree[2 * k + 2])

    def prod(self, a, b, k=0, ll=0, rr=None):
        """
        区間 [a, b) の演算結果を返す。O(log n)
        k は今見ている内部 index の番号、[ll, rr) は self.tree[k] が表す区間。
        """
        if rr is None:
            rr = self.size2
        self._eval(k)
        if rr <= a or b <= ll:
            return self.e
        elif a <= ll and rr <= b:
            return self.tree[k]
        else:
            vl = self.prod(a, b, 2 * k + 1, ll, (ll + rr) // 2)
            vr = self.prod(a, b, 2 * k + 2, (ll + rr) // 2, rr)
            return op(vl, vr)


T = LazySegtree(n)

for i in range(n):
    T.update(i, (A[i] << 32) + 1)


for i in range(q):
    if Q[i][0] == 0:
        l, r, b, c = tuple(Q[i][1:])
        T.apply(l, r, (b << 32) + c)
    else:
        l, r = tuple(Q[i][1:])
        print(T.prod(l, r) >> 32)

    # update メソッドのテストのため、わざと毎回全部 1 (タプル (0, 1) の整数表現) にしている
    for j in range(n):
        T.update(j, 1)


# 問題
# https://judge.yosupo.jp/problem/range_affine_range_sum

# 入力
# 5 2
# 1 2 3 4 5
# 0 2 4 100 101
# 1 0 3

# update (旧) 使用時の出力 (全部 0 に更新した後に、遅延していた作用 (取り消されるべきだが残っている) が行われるため、誤ってしまう)
# 101

# update (新) 使用時の出力 (正しい)
# 0
