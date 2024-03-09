# 「1, DFS + オイラーツアー + セグメント木」「2, BFS か DFS + ダブリング」の 2 つの方法がある。基本的に 1 が速いはず。

# 1, DFS + オイラーツアー + セグメント木

# n: 木の頂点数
# P: 各頂点の親のリスト

shift = 30
big = 10**7  # 頂点数以上

mask = (1 << shift) - 1


def op(x0, x1):
    return min(x0, x1)


def e():
    return big << 30


from segment_tree import Segtree  # ここにセグメント木を貼る  # noqa

# 隣接リストを作る
M = [[] for _ in range(n)]
for i in range(n - 1):
    M[P[i]].append(i + 1)
    M[i + 1].append(P[i])


P = [-1] * n  # iの親ノードの番号（最短路などの復元用）
D = [-1] * n  # 始点からiまでの最短距離（兼訪問フラグ）

V = []  # 頂点に入ったとき・戻ってきたとき (出たときを含む) に、頂点番号を記録する
vind = 0

vind_in = [-1] * n  # 頂点に入ったときの V の index
vind_out = [-1] * n  # 頂点から出たときの V の index


def dfs(i, next_ind):
    """非再帰 DFS"""
    global vind
    if next_ind == 0:
        V.append(i)
        vind_in[i] = vind
        vind += 1
    else:
        V.append(i)
        vind += 1

    ST[-1] = (i, next_ind + 1)

    if next_ind < len(M[i]):
        x = M[i][next_ind]
        if D[x] == -1:
            D[x] = D[i] + 1
            P[x] = i
            ST.append((x, 0))
    else:
        vind_out[i] = vind
        V.append(i)
        vind += 1
        ST.pop()


s = 0  # 始点の番号
D[s] = 0


# オイラーツアー
ST = [(s, 0)]
while len(ST) > 0:
    dfs(*ST[-1])

# セグ木には、最小値とその index を持たせる
S = Segtree(len(V))

for i in range(len(V)):
    S.update(i, D[V[i]] << 30 | i)


def lca(i, j):
    """頂点 i, j の lowest common ancestor (最小共通祖先) を求める"""
    a = vind_in[i]
    b = vind_in[j]
    if a > b:
        a, b = b, a
    return V[S.prod(a, b + 1) & mask]


def tree_dist(i, j):
    """頂点 i, j 間の距離を求める"""
    return D[i] + D[j] - D[lca(i, j)] * 2


# 2, BFS か DFS + ダブリング

# n: 木の頂点数
# P: 各頂点の親のリスト
# D: 各頂点の根からの距離のリスト

le = 20  # log2(n) 以上

PS = [[-1] * le for i in range(n)]  # 頂点 i の 2^j 個祖先の頂点を保存

for i in range(n):
    PS[i][0] = P[i]
for i in range(1, le):
    for j in range(n):
        if PS[j][i - 1] != -1:
            PS[j][i] = PS[PS[j][i - 1]][i - 1]


def lca(i, j):
    """頂点 i, j の lowest common ancestor (最小共通祖先) を求める"""
    # i と j の根からの距離を揃える
    if D[i] > D[j]:
        i, j = j, i
    d = D[j] - D[i]
    ind = 0
    while d > 0:
        if d % 2 == 1:
            j = PS[j][ind]
        d //= 2
        ind += 1

    # 距離を揃えた時点で一致すればそれが LCA
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


def tree_dist(i, j):
    """頂点 i, j 間の距離を求める"""
    return D[i] + D[j] - D[lca(i, j)] * 2
