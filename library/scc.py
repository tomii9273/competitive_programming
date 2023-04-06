# 参考: https://mathtrain.jp/kyorenketsu#:~:text=%E5%BC%B7%E9%80%A3%E7%B5%90%E6%88%90%E5%88%86%E5%88%86%E8%A7%A3%E3%81%A8,%E9%80%A3%E7%B5%90%E6%88%90%E5%88%86%EF%BC%89%E3%81%AB%E5%B1%9E%E3%81%97%E3%81%BE%E3%81%99%E3%80%82

# 注意: https://atcoder.jp/contests/practice2/tasks/practice2_g で 2850 ms (制限時間 5000 ms)
# 1000 ms 台の人も多いので、もっと速くできそう


class scc:  # 有向グラフを強連結成分分解（互いに行き来できる領域ごとに区切る）する。
    def __init__(self, n):  # 頂点数nのグラフを作成
        self.n = n
        self.M = [[] for i in range(n)]
        self.IM = [[] for i in range(n)]

    def add_edge(self, frm, to):  # frm->toの辺を追加
        self.M[frm].append(to)
        self.IM[to].append(frm)

    # DFSしながら頂点stと同じ連結成分の頂点に番号を付けていく（この関数は連結成分ごとに呼ばれる）。
    # ANSは1頂点に対し一対一で付けた番号を保存するリスト、初期番号はcnt
    # Vは連結成分ごとに付けた番号を保存するリスト、番号はv
    def _dfs_numbering(self, st, M, V, ANS, cnt, v):
        ST = [st]
        while len(ST) > 0:
            i = ST[-1]
            if ANS[i] == -1:
                V[i] = v
                end = 1
                for x in M[i]:
                    if V[x] == -1:
                        ST.append(x)
                        end = 0
                if end == 1:
                    ST.pop()
                    ANS[i] = cnt
                    cnt += 1
            else:
                ST.pop()
        return cnt

    def scc_list(self):  # 連結成分ごとの頂点リストを返す
        n = self.n
        V = [-1] * n
        ANS = [-1] * n

        cnt = 0
        for i in range(n):
            if V[i] == -1:
                cnt = self._dfs_numbering(i, self.M, V, ANS, cnt, 0)

        ANS1 = [-1] * n
        for i in range(n):
            ANS1[ANS[i]] = i

        V = [-1] * n
        ANS = [-1] * n
        v = 0
        for i in range(n - 1, -1, -1):
            if V[ANS1[i]] == -1:
                _ = self._dfs_numbering(ANS1[i], self.IM, V, ANS, 0, v)
                v += 1

        FANS = [[] for i in range(v)]
        for i in range(n):
            FANS[V[i]].append(i)

        return FANS
