# 定数倍でTLEすることがある。ACLのsegtreeを使ったほうがよい。


def e():
    # 単位元を返すようにする。以下は最小値を求める場合の例。
    return float("inf")


def op(a, b):
    # 木に入っているもの a, b の演算を返すようにする (演算は結合法則を満たす必要があるが、可換でなくてもよい) 。以下は最小値を求める場合の例。
    return min(a, b)


class Segtree:
    def __init__(self, n):
        # sizeは最初に定めたサイズ、size2は2の累乗の値をとるサイズ(>=size)
        self.size = n
        i = 1
        while i < n:
            i *= 2
        self.tree = [e() for _ in range(2 * i - 1)]
        self.size2 = i
        self.f = e()

    def __getitem__(self, i):  # [i]でi番目の値を得られるようにした
        if i < 0:
            i %= self.size
        return self.op(i, i + 1)

    def update(self, i, x):  # i番目の値をxに更新
        j = self.size2 + i - 1
        self.tree[j] = x
        while j > 0:
            j = (j - 1) // 2
            self.tree[j] = op(self.tree[2 * j + 1], self.tree[2 * j + 2])

    def op(self, a, b, k=0, ll=0, rr=None):  # 区間[a, b)の演算結果を返す
        if rr is None:
            rr = self.size2
        if rr <= a or b <= ll:
            return self.f
        elif a <= ll and rr <= b:
            return self.tree[k]
        else:
            vl = self.op(a, b, 2 * k + 1, ll, (ll + rr) // 2)
            vr = self.op(a, b, 2 * k + 2, (ll + rr) // 2, rr)
            return op(vl, vr)


class SegtreeMin:  # 最小値を求める用
    def __init__(self, n, f=float("inf")):
        # sizeは最初に定めたサイズ、size2は2の累乗の値をとるサイズ(>=size)、fは初期値
        self.size = n
        i = 1
        while i < n:
            i *= 2
        self.tree = [f] * (2 * i - 1)
        self.size2 = i
        self.f = f

    def __getitem__(self, i):  # [i]でi番目の値を得られるようにした
        if i < 0:
            i %= self.size
        return self.get(i, i + 1)

    def update(self, i, x):  # i番目の値をxに更新(xは更新前の値より小さくなければならない)
        j = self.size2 + i - 1
        self.tree[j] = x
        while j > 0:
            j = (j - 1) // 2
            self.tree[j] = min(self.tree[2 * j + 1], self.tree[2 * j + 2])
            # print(self.tree)

    def get(self, a, b, k=0, ll=0, rr=None):  # 区間[a, b)の最小値を返す
        if rr is None:
            rr = self.size2
        if rr <= a or b <= ll:
            return self.f
        elif a <= ll and rr <= b:
            return self.tree[k]
        else:
            # print(2*k+1, 2*k+2,l, (l+r)//2,r)
            vl = self.get(a, b, 2 * k + 1, ll, (ll + rr) // 2)
            vr = self.get(a, b, 2 * k + 2, (ll + rr) // 2, rr)
            return min(vl, vr)


class SegtreeMax:  # 最大値を求める用
    def __init__(self, n, f=-float("inf")):
        # sizeは最初に定めたサイズ、size2は2の累乗の値をとるサイズ(>=size)、fは初期値
        self.size = n
        i = 1
        while i < n:
            i *= 2
        self.tree = [f] * (2 * i - 1)
        self.size2 = i
        self.f = f

    def __getitem__(self, i):  # [i]でi番目の値を得られるようにした
        if i < 0:
            i %= self.size
        return self.get(i, i + 1)

    def update(self, i, x):  # i番目の値をxに更新 (xは更新前の値より大きくなければならないわけではなさそう？)
        j = self.size2 + i - 1
        self.tree[j] = x
        while j > 0:
            j = (j - 1) // 2
            self.tree[j] = max(self.tree[2 * j + 1], self.tree[2 * j + 2])
            # print(self.tree)

    def get(self, a, b, k=0, ll=0, rr=None):  # 区間[a, b)の最大値を返す
        if rr is None:
            rr = self.size2
        if rr <= a or b <= ll:
            return self.f
        elif a <= ll and rr <= b:
            return self.tree[k]
        else:
            # print(2*k+1, 2*k+2,l, (l+r)//2,r)
            vl = self.get(a, b, 2 * k + 1, ll, (ll + rr) // 2)
            vr = self.get(a, b, 2 * k + 2, (ll + rr) // 2, rr)
            return max(vl, vr)


# T = segtree(6)
# T.update(1, 4)
# T.update(3, 2)
# T.update(4, 1)
# for i in range(8+1):
#     print(i, T.get(0, i))
# print(T.size)
# print(T.size2)


# 2次元セグメント木(最大値専用)。かなり遅いので注意。PyPyよりPythonで提出する方が良いかも。


class Segtree2DMax:
    def __init__(self, h, w, f=-float("inf")):
        self.size = h
        i = 1
        while i < h:
            i *= 2
        self.tree = [SegtreeMax(w) for _ in range(2 * i - 1)]
        self.size2 = i
        self.f = f

    def update(self, i0, i1, x):
        j = self.size2 + i0 - 1
        self.tree[j].update(i1, x)
        while j > 0:
            j = (j - 1) // 2
            self.tree[j].update(i1, max(self.tree[2 * j + 1].get(i1, i1 + 1), self.tree[2 * j + 2].get(i1, i1 + 1)))

    def get(self, a, b, c, d, k=0, ll=0, rr=None):  # [a, b)行内の区間[c, d)の最大値を返す
        if rr is None:
            rr = self.size2
        if rr <= a or b <= ll:
            return self.f
        elif a <= ll and rr <= b:
            return self.tree[k].get(c, d)
        else:
            vl = self.get(a, b, c, d, 2 * k + 1, ll, (ll + rr) // 2)
            vr = self.get(a, b, c, d, 2 * k + 2, (ll + rr) // 2, rr)
            return max(vl, vr)
