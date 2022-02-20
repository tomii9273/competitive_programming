class UnionFind:  # DSU（disjoint set union, 素集合データ構造）と同じ
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n
        self.min_index_for_leader = [i for i in range(n)]
        self.max_index_for_leader = [i for i in range(n)]

    def leader(self, x):  # xが属する連結成分の代表元
        if self.parents[x] < 0:
            return x
        else:
            self.parents[x] = self.leader(self.parents[x])
            return self.parents[x]

    def size(self, x):  # xが属する連結成分のサイズ
        return -self.parents[self.leader(x)]

    def merge(self, x, y):  # xとyを辺でつなぐ、残ったほうの代表元を返す
        x = self.leader(x)
        y = self.leader(y)
        if x == y:
            return x
        if self.parents[x] > self.parents[y]:
            x, y = y, x
        self.parents[x] += self.parents[y]
        self.parents[y] = x
        self.min_index_for_leader[x] = min(self.min_index_for_leader[x], self.min_index_for_leader[y])
        self.max_index_for_leader[x] = max(self.max_index_for_leader[x], self.max_index_for_leader[y])
        return x

    def same(self, x, y):  # xとyが連結かどうか
        return self.leader(x) == self.leader(y)

    def groups(self):  # 連結成分ごとの頂点リスト
        n = self.n
        leader_index = [-1] * n
        ind = 0
        for i in range(n):
            if self.parents[i] < 0:
                leader_index[i] = ind
                ind += 1
        ANS = [[] for i in range(ind)]
        for i in range(n):
            ld = self.leader(i)
            ANS[leader_index[ld]].append(i)
        return ANS

    def n_cc(self):  # グラフ全体の連結成分の数
        A = [i for i in self.parents if i < 0]
        return len(A)

    def min_index(self, x):  # xが属する連結成分の最小の元
        return self.min_index_for_leader[self.leader(x)]

    def max_index(self, x):  # xが属する連結成分の最大の元
        return self.max_index_for_leader[self.leader(x)]
