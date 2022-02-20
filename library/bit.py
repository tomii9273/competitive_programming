# ACLに伴い0-indexedに直した
class Bit:  # Fenwick Tree と同じ
    def __init__(self, n):
        self.size = n
        self.tree = [0] * (n + 1)

    def __getitem__(self, i):  # [i]でi番目の値を得られるようにした
        if i < 0:
            i %= self.size
        return self.sum(i, i + 1)

    def sum(self, ll=0, rr=10 ** 9):  # [ll, rr)の和を求める
        # 内部的には[ll+1, rr+1)の和、つまり(rrまでの和)-(llまでの和)
        rr = min(rr, self.size)
        s = 0
        while rr > 0:
            s += self.tree[rr]
            rr -= rr & -rr  # 2進数の最も下位の1を取り除くという意味(例:1010→1000)
        while ll > 0:
            s -= self.tree[ll]
            ll -= ll & -ll  # 2進数の最も下位の1を取り除くという意味(例:1010→1000)
        return s

    def val(self, i):  # i番目の値を返す
        return self.sum(i, i + 1)

    def add(self, i, x):  # i番目にxを足す
        i += 1
        while i <= self.size:
            self.tree[i] += x
            i += i & -i  # 2進数の最も下位の1を繰り上げるという意味(例:1010→1100)

    def sett(self, i, x):  # i番目をxにする
        self.add(i, x - self.sum(i, i + 1))

    def print_bit(self):  # 内部状態をindex順に出力
        print([self.sum(i, i + 1) for i in range(self.size)])

    def print_sum(self):  # 累積和をindex順に出力
        print([self.sum(0, i + 1) for i in range(self.size)])

    def lower_bound_left(self, w):  # xまでの和がw以上となる最小のx、総和がw未満の場合nが返る
        n = self.size
        r = 1
        x = 0
        if self.sum(0, n) < w:
            return n
        while r < n:
            r *= 2
        le = r
        while le > 0:
            if x + le < n and self.tree[x + le] < w:
                w -= self.tree[x + le]
                x += le
            le //= 2
        return x

    def upper_bound_left(self, w):  # xまでの和がwより大きくなる最小のx、総和がw以下の場合nが返る
        n = self.size
        r = 1
        x = 0
        if self.sum(0, n) <= w:
            return n
        while r < n:
            r *= 2
        le = r
        while le > 0:
            if x + le < n and self.tree[x + le] <= w:
                w -= self.tree[x + le]
                x += le
            le //= 2
        return x

    def lower_bound_right(self, w):  # xまでの和がw以下となる最大のx、0番目がwより大きい場合-1が返る
        return self.upper_bound_left(w) - 1

    def upper_bound_right(self, w):  # xまでの和がw未満となる最大のx、0番目がw以上の場合-1が返る
        return self.lower_bound_left(w) - 1


class Bit2d:  # 2次元BIT
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.tree = [Bit(w) for i in range(h + 1)]

    def add(self, i, j, x):  # i行j列にxを足す
        i += 1
        while i <= self.h:
            self.tree[i].add(j, x)
            i += i & -i

    def sum0(self, i, j):  # [0,i)行内の[0,j)列の総和
        s = 0
        while i > 0:
            s += self.tree[i].sum(0, j)
            i -= i & -i
        return s

    def sum1(self, i0, i1, j0, j1):  # [i0,i1)行内の[j0,j1)列の総和
        return self.sum0(i1, j1) - self.sum0(i0, j1) - self.sum0(i1, j0) + self.sum0(i0, j0)

    def print_bit(self):  # 内部状態を出力
        print([[self.sum1(i, i + 1, j, j + 1) for j in range(self.w)] for i in range(self.h)])

    def print_sum(self):  # 2次元累積和を出力
        print([[self.sum0(i + 1, j + 1) for j in range(self.w)] for i in range(self.h)])


# B = Bit(8)
# for i in [0,2,3,7]:
#     B.add(i, 1)
# print(B.tree)
# print(B.sum(0,4))
# B.print_bit()
# B.print_sum()
# nn = 4
# print(B.lower_bound_left(nn))
# print(B.upper_bound_left(nn))
# print(B.lower_bound_right(nn))
# print(B.upper_bound_right(nn))


# C = Bit2d(5,3)
# C.print_bit()
# C.add(2,1,1)
# C.add(3,1,-3)
# C.add(0,0,2)
# C.print_bit()
# C.print_sum()
