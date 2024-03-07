class UnionFind:
    """
    DSU (disjoint set union, 素集合データ構造) と同じ。
    union by size と経路圧縮の両方を導入しており、基本的な操作が O(alpha(n)) で行える。
    """

    def __init__(self, n: int):
        """
        n: サイズ
        構築は O(n) で行われる。
        """
        self.n = n
        self.parents = [-1] * n
        self.min_index_for_leader = [i for i in range(n)]
        self.max_index_for_leader = [i for i in range(n)]
        self._n_cc = n

    def leader(self, x: int) -> int:
        """x が属する連結成分の代表元。O(alpha(n))"""
        path = []
        while x >= 0:
            path.append(x)
            ans = x
            x = self.parents[x]
        for v in path[:-1]:  # 経路圧縮
            self.parents[v] = ans
        return ans

    def size(self, x: int) -> int:
        """x が属する連結成分のサイズ。O(alpha(n))"""
        return -self.parents[self.leader(x)]

    def merge(self, x: int, y: int) -> int:
        """x と y を辺でつなぐ (union by size)。残ったほうの代表元を返す。O(alpha(n))"""
        x = self.leader(x)
        y = self.leader(y)
        if x == y:
            return x
        self._n_cc -= 1
        if self.parents[x] > self.parents[y]:
            x, y = y, x
        # self.parents[x] <= self.parents[y] であり、(x の木のサイズ) >= (y の木のサイズ) である
        self.parents[x] += self.parents[y]
        self.parents[y] = x
        self.min_index_for_leader[x] = min(self.min_index_for_leader[x], self.min_index_for_leader[y])
        self.max_index_for_leader[x] = max(self.max_index_for_leader[x], self.max_index_for_leader[y])
        return x

    def same(self, x: int, y: int) -> bool:
        """x と y が連結かどうか。O(alpha(n))"""
        return self.leader(x) == self.leader(y)

    def groups(self) -> list[int]:
        """連結成分ごとの頂点リスト。O(n alpha(n))"""
        n = self.n
        leader_index = [-1] * n
        ind = 0
        for i in range(n):
            if self.parents[i] < 0:
                leader_index[i] = ind
                ind += 1
        ANS = [[] for _ in range(ind)]
        for i in range(n):
            ld = self.leader(i)
            ANS[leader_index[ld]].append(i)
        return ANS

    def n_cc(self) -> int:
        """グラフ全体の連結成分の数。O(1)"""
        return self._n_cc

    def min_index(self, x: int) -> int:
        """x が属する連結成分の最小の元。O(alpha(n))"""
        return self.min_index_for_leader[self.leader(x)]

    def max_index(self, x: int) -> int:
        """x が属する連結成分の最大の元。O(alpha(n))"""
        return self.max_index_for_leader[self.leader(x)]


from persistent_array import Node, PersistentArray  # noqa


class PersistentUnionFind:
    """
    全永続 Union-Find。
    union by size を導入している。(経路圧縮は永続配列を update するため逆に遅くなる・MLE の原因になる可能性があるので、導入していない)
    """

    def __init__(self, n: int, big: int = 10**6, first_ver: int = 0):
        """
        n: サイズ
        big: 今後登場する最大の version 番号より大きい値を入れる。merge で 2 回 update する際に一時的に使う。
        first_ver: 最初の version 番号
        構築は O(n) で行われる。
        """
        self.n = n
        self.big = big
        self.parents = PersistentArray(n, -1, None, first_ver)
        self._n_cc = [-1] * first_ver + [0]

    def leader(self, t: int, x: int) -> int:
        """version t で x が属する連結成分の代表元。O((log n)^2)"""
        while x >= 0:
            ans = x
            x = self.parents[t, x]
        return ans

    def size(self, t: int, x: int) -> int:
        """version t で x が属する連結成分のサイズ。O((log n)^2)"""
        return -self.parents[self.leader(t, x)]

    def merge(self, t_old: int, t_new: int, x: int, y: int) -> int:
        """
        version t_old で x と y を辺でつないだ (union by size) ものを version t_new とする。
        既につながっている場合はコピーになる。残ったほうの代表元を返す。O((log n)^2 + big)
        """
        x = self.leader(t_old, x)
        y = self.leader(t_old, y)
        if x == y:
            self.parents.copy(t_old, t_new)
            return x
        self._n_cc += [-1] * (t_new - len(self._n_cc) + 1)
        self._n_cc[t_new] = self._n_cc[t_old] - 1
        if self.parents[t_old, x] > self.parents[t_old, y]:
            x, y = y, x
        # self.parents[t_old, x] <= self.parents[t_old, y] であり、(x の木のサイズ) >= (y の木のサイズ) である
        self.parents.update(t_old, t_new + self.big, x, self.parents[t_old, x] + self.parents[t_old, y])
        self.parents.update(t_new + self.big, t_new, y, x)
        return x

    def same(self, t: int, x: int, y: int) -> bool:
        """version t で x と y が連結かどうか。O((log n)^2)"""
        return self.leader(t, x) == self.leader(t, y)

    def groups(self, t: int) -> list[int]:
        """version t での連結成分ごとの頂点リスト。O(n log n)"""
        n = self.n
        parents_t = self.parents.get_all(t)
        leader_index = [-1] * n
        ind = 0
        for i in range(n):
            if parents_t[i] < 0:
                leader_index[i] = ind
                ind += 1
        ANS = [[] for _ in range(ind)]
        for i in range(n):
            x = i
            while x >= 0:
                x = parents_t[x]
            ANS[leader_index[x]].append(i)
        return ANS

    def n_cc(self, t: int) -> int:
        """version t でのグラフ全体の連結成分の数。O(1)"""
        return self._n_cc[t]
