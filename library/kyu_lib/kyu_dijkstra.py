# O((V + E)log(V))
# Cは [[スタート頂点, ゴール頂点, 重み], ...] のリスト

M = [[] for i in range(n)]
for i in range(len(C)):
    M[C[i][0]].append([C[i][1], C[i][2]])  # 無向グラフなら両方追加
    M[C[i][1]].append([C[i][0], C[i][2]])  # 無向グラフなら両方追加

import heapq

D = [float("inf")] * n  # 頂点0からの距離
P = [-1] * n  # 頂点0からの最短距離において、そこの直前の頂点(経路復元に利用)
D[0] = 0
V = [0] * n  # その頂点のD[i]が最短距離と確定したら1
Q = []  # 優先度付きキュー
for v in range(n):
    heapq.heappush(Q, [D[v], v])

le = len(Q)
while le > 0:
    q = heapq.heappop(Q)
    u = q[1]
    du = q[0]
    if V[u] == 0:
        V[u] = 1
        le -= 1
        for i in range(len(M[u])):
            v = M[u][i][0]
            luv = M[u][i][1]
            if V[v] == 0:
                alt = du + luv
                if D[v] > alt:
                    D[v] = alt
                    P[v] = u
                    heapq.heappush(Q, [alt, v])