# dfs_no_recursion.py が dfs_tree_parent_distance_descendant.py と同様に動くかの確認

import sys
sys.setrecursionlimit(10 ** 9)  # Codeforcesでは350000程度に
def input(): return sys.stdin.readline().strip()


# n頂点の木をランダムに作成し、辺のリスト(1-indexed)を返す。
def make_random_tree(n):
    from random import randint, shuffle
    A = []
    for i in range(n-1):
        A.append([randint(1, i+1), i+2])
    B = [i for i in range(n)]
    shuffle(B)
    for i in range(n-1):
        for j in range(2):
            A[i][j] = B[A[i][j]-1] + 1
        shuffle(A[i])
    shuffle(A)
    return A


n = 100
C = make_random_tree(n)

for i in range(len(C)):  # 入力が 1-indexed の場合
    for j in range(2):
        C[i][j] -= 1


M = [[] for i in range(n)]
for i in range(n-1):
    M[C[i][0]].append(C[i][1])
    M[C[i][1]].append(C[i][0])  # 有向グラフの場合は削除！！

# print(M)

P = [-1] * n  # iの親ノードの番号（最短路などの復元用）
D = [-1] * n  # 始点からiまでの最短距離（兼訪問フラグ）
DN = [-1] * n  # i以深のノード総数（i自身も含める）
V_in = []  # 入った順に頂点番号を記録
V_out = []  # 出た順に頂点番号を記録


def dfs(i, d):
    V_in.append(i)
    dn = 1
    for x in M[i]:
        if D[x] == -1:
            D[x] = d+1
            P[x] = i
            dn += dfs(x, d+1)
    DN[i] = dn
    V_out.append(i)
    return dn


s = 0  # 始点の番号
D[s] = 0

dfs(s, 0)


P_1 = [-1] * n  # iの親ノードの番号（最短路などの復元用）
D_1 = [-1] * n  # 始点からiまでの最短距離（兼訪問フラグ）
DN_1 = [1] * n  # i以深のノード総数（i自身も含める）
V_in_1 = []  # 入った順に頂点番号を記録
V_out_1 = []  # 出た順に頂点番号を記録


def dfs_1(i, d):
    V_in_1.append(i)
    for j in range(len(M[i])-1, -1, -1):
        x = M[i][j]
        if D_1[x] == -1:
            D_1[x] = d+1
            P_1[x] = i
            ST.append((x, d+1))
            end_count[i] += 1


def do_end(i, p):
    V_out_1.append(i)
    for x in M[i]:
        if x != p:
            DN_1[i] += DN_1[x]
    if p != -1:
        end_count[p] -= 1
    if end_count[p] == 0:
        return p
    return -1


s = 0  # 始点の番号
D_1[s] = 0
ST = [(s, 0)]
end_count = [0] * n
while len(ST) > 0:
    i, d = ST.pop()
    dfs_1(i, d)
    while i != -1 and end_count[i] == 0:
        i = do_end(i, P_1[i])

assert P == P_1
assert D == D_1
assert DN == DN_1
assert V_in == V_in_1
assert V_out == V_out_1
