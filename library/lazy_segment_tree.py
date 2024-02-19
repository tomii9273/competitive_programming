# 以下の op, e, mapping, composition, id は、区間に x を加算し、区間最小値を求める (Range Add Range Min) ような遅延評価セグメント木を作る場合の例。


def op(x0, x1):
    # 木に入っているもの x0, x1 の演算を返すようにする (演算は結合法則を満たす必要があるが、可換でなくてもよい) 。
    return min(x0, x1)


def e():
    # op の単位元を返す。
    return float("inf")


def mapping(x, f):
    # 木に入っているもの x に関数 f を作用させる。
    return x + f


def composition(f0, f1):
    # 関数 f0 と f1 の合成 (f0 をしてから f1 をする、という順序) (演算は結合法則を満たす必要があるが、可換でなくてもよい) 。
    return f0 + f1


def id():
    # composition の単位元を返す。
    return 0


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
        self.mapping = mapping
        self.composition = composition
        self.op = op
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
            self.lazy[2 * k + 1] = self.composition(self.lazy[2 * k + 1], lazy_k)
            self.lazy[2 * k + 2] = self.composition(self.lazy[2 * k + 2], lazy_k)
        self.tree[k] = self.mapping(self.tree[k], lazy_k)
        self.lazy[k] = self.id

    def update(self, i, x):
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
            self.tree[j] = self.op(self.tree[2 * j + 1], self.tree[2 * j + 2])

    def apply(self, a, b, x, k=0, ll=0, rr=None):
        """
        区間 [a, b) に x を作用させる。O(log n)
        k は今見ている内部 index の番号、[ll, rr) は self.tree[k] が表す区間。
        """
        if rr is None:
            rr = self.size2
        self._eval(k)
        if a <= ll and rr <= b:
            self.lazy[k] = self.composition(self.lazy[k], x)
            self._eval(k)
        elif a < rr and ll < b:  # [ll, rr) が [a, b) に含まれないが、共通部分はある場合
            self.apply(a, b, x, 2 * k + 1, ll, (ll + rr) // 2)
            self.apply(a, b, x, 2 * k + 2, (ll + rr) // 2, rr)
            self.tree[k] = self.op(self.tree[2 * k + 1], self.tree[2 * k + 2])

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
            return self.op(vl, vr)
