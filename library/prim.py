from heapq import heappush, heappop

# O((V+E)logV) = O(ElogV)
# Eは[始点, 終点, 重み]のリスト。始点と終点を逆にしたものが入っている必要はない。

M = [[] for i in range(n)]
for i in range(len(E)):
    M[E[i][0]].append((E[i][1], E[i][2]))
    M[E[i][1]].append((E[i][0], E[i][2]))

E_new = []  # 最小全域木の(始点, 終点, 重み)が入るリスト
sum_w = 0  # 最小全域木の重みの合計(構成できなかったら-1)
Q = []
V_is_used = [False] * n

s = 0  # 始点(どこでも良い)
V_is_used[s] = True

for i in range(len(M[s])):
    heappush(Q, (M[s][i][1], s, M[s][i][0]))

for i in range(n - 1):
    while len(Q) > 0 and (V_is_used[Q[0][1]] and V_is_used[Q[0][2]]):
        heappop(Q)

    if len(Q) == 0:  # 最小全域木を構成できなかったら-1
        sum_w = -1
        break

    w, ind0, ind1 = heappop(Q)
    E_new.append((ind0, ind1, w))
    sum_w += w

    if V_is_used[ind0]:
        V_is_used[ind1] = True
        for j in range(len(M[ind1])):
            if not V_is_used[M[ind1][j][0]]:
                heappush(Q, (M[ind1][j][1], ind1, M[ind1][j][0]))
    else:
        V_is_used[ind0] = True
        for j in range(len(M[ind0])):
            if not V_is_used[M[ind0][j][0]]:
                heappush(Q, (M[ind0][j][1], ind0, M[ind0][j][0]))

print(sum_w)
