class UnionFind:
    """DSU (disjoint set union, 素集合データ構造) と同じ。"""

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
        """x が属する連結成分の代表元。O(log n)"""
        while x >= 0:
            ans = x
            x = self.parents[x]
        return ans

    def size(self, x: int) -> int:
        """x が属する連結成分のサイズ。O(log n)"""
        return -self.parents[self.leader(x)]

    def merge(self, x: int, y: int) -> int:
        """x と y を辺でつなぐ。残ったほうの代表元を返す。O(log n)"""
        x = self.leader(x)
        y = self.leader(y)
        if x == y:
            return x
        self._n_cc -= 1
        if self.parents[x] > self.parents[y]:
            x, y = y, x
        self.parents[x] += self.parents[y]
        self.parents[y] = x
        self.min_index_for_leader[x] = min(self.min_index_for_leader[x], self.min_index_for_leader[y])
        self.max_index_for_leader[x] = max(self.max_index_for_leader[x], self.max_index_for_leader[y])
        return x

    def same(self, x: int, y: int) -> bool:
        """x と y が連結かどうか。O(log n)"""
        return self.leader(x) == self.leader(y)

    def groups(self) -> list[int]:
        """連結成分ごとの頂点リスト。O(n log n)"""
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
        """x が属する連結成分の最小の元。O(log n)"""
        return self.min_index_for_leader[self.leader(x)]

    def max_index(self, x: int) -> int:
        """x が属する連結成分の最大の元。O(log n)"""
        return self.max_index_for_leader[self.leader(x)]
