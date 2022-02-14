# O(ElogE)
# ここにUnionFindを貼る

E.sort(key=lambda x: x[2])
# Eは[始点, 終点, 重み]のリスト。始点と終点を逆にしたものが入っている必要はない。

E_new = []  # 最小全域木の(始点, 終点, 重み)が入るリスト
sum_w = 0  # 最小全域木の重みの合計(構成できなかったら-1)

U = UnionFind(n)
e = 0
for i in range(len(E)):
    if e == n-1:
        break
    if U.leader(E[i][0]) != U.leader(E[i][1]):
        U.merge(E[i][0], E[i][1])
        E_new.append(tuple(E[i]))
        sum_w += E[i][2]
        e += 1

if U.n_cc() != 1:  # 最小全域木を構成できなかったら-1
    sum_w = -1

print(sum_w)
