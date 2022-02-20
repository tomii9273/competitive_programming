# O((V+E)logV) = O(ElogV)
# Cは [[スタート頂点, ゴール頂点, 重み], ...] のリスト

from heapq import heappush, heappop

M = [[] for i in range(n)]
for i in range(len(C)):
    M[C[i][0]].append((C[i][1], C[i][2]))
    M[C[i][1]].append((C[i][0], C[i][2]))  # 有向グラフの場合は削除！！
for i in range(n):
    M[i] = tuple(M[i])
M = tuple(M)  # しない方が速い場合もある


s = 0  # 始点の番号
big = 10 ** 20  # 距離infを示す数(必要以上に大きくしない)

D = [big] * n  # 頂点sからの距離
P = [-1] * n  # 頂点sからの最短距離において、そこの直前の頂点(経路復元に利用)
D[s] = 0
V = [0] * n  # その頂点のD[i]が最短距離と確定したら1
Q = []  # 優先度付きキュー
heappush(Q, (0, s))

while len(Q) > 0:
    q = heappop(Q)
    u = q[1]
    du = q[0]
    if V[u] == 0:
        V[u] = 1
        for i in range(len(M[u])):
            v = M[u][i][0]
            luv = M[u][i][1]
            if V[v] == 0:
                alt = du + luv
                if D[v] > alt:
                    D[v] = alt
                    P[v] = u
                    heappush(Q, (alt, v))
