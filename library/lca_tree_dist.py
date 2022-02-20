# n: 木の頂点数
# P: 各頂点の親のリスト
# D: 各頂点の根からの距離のリスト

le = 20  # log2(n)以上

PS = [[-1] * le for i in range(n)]  # 頂点iの2^j個祖先の頂点を保存

for i in range(n):
    PS[i][0] = P[i]
for i in range(1, le):
    for j in range(n):
        if PS[j][i - 1] != -1:
            PS[j][i] = PS[PS[j][i - 1]][i - 1]


def lca(i, j):  # iとjの最小共通祖先を求める
    # iとjの根からの距離を揃える
    if D[i] > D[j]:
        i, j = j, i
    d = D[j] - D[i]
    ind = 0
    while d > 0:
        if d % 2 == 1:
            j = PS[j][ind]
        d //= 2
        ind += 1

    if i == j:
        return i

    ans = 0
    mul = 2 ** (len(PS[i]) - 1)
    for ind in range(len(PS[0]) - 1, -1, -1):
        if PS[i][ind] != -1 and PS[i][ind] != PS[j][ind]:
            ans += mul
            i = PS[i][ind]
            j = PS[j][ind]
        mul //= 2

    return P[i]


def tree_dist(i, j):  # iとjの距離を求める
    return D[i] + D[j] - D[lca(i, j)] * 2
