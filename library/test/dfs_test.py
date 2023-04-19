# dfs_no_recursion.py が dfs_tree_parent_distance_descendant.py と同様に動くかの確認

import os
import sys

sys.path.append(os.pardir)  # 親ディレクトリ内のファイルをインポートするのに必要

sys.setrecursionlimit(10 ** 9)  # Codeforcesでは350000程度に


def input():
    return sys.stdin.readline().strip()


from make_random_graph import make_random_graph

n = 20
C = make_random_graph(n)

M = [[] for i in range(n)]
for i in range(len(C)):
    M[C[i][0]].append(C[i][1])
    M[C[i][1]].append(C[i][0])

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
            D[x] = d + 1
            P[x] = i
            dn += dfs(x, d + 1)
    DN[i] = dn
    V_out.append(i)
    return dn


s = 0  # 始点の番号
D[s] = 0

dfs(s, 0)


P_1 = [-1] * n  # iの親ノードの番号（最短路などの復元用）
D_1 = [-1] * n  # 始点からiまでの最短距離（兼訪問フラグ）
DN_1 = [-1] * n  # i以深のノード総数（i自身も含める）
V_in_1 = []  # 入った順に頂点番号を記録
V_out_1 = []  # 出た順に頂点番号を記録
# print(DN_1)


def dfs_1(i, next_ind):
    if next_ind == len(M[i]):
        V_out_1.append(i)
        DN_1[i] = 1
        for x in M[i]:
            if P_1[x] == i:
                DN_1[i] += DN_1[x]
                # print(i, x, DN_1[x], P_1[i])
        ST.pop()
    else:
        x = M[i][next_ind]
        if D_1[x] != -1:
            ST[-1] = (i, next_ind + 1)
        else:
            D_1[x] = D_1[i] + 1
            P_1[x] = i
            V_in_1.append(x)
            ST.append((x, 0))


s = 0  # 始点の番号
D_1[s] = 0
V_in_1.append(s)
ST = [(s, 0)]
while len(ST) > 0:
    dfs_1(*ST[-1])

# print(DN)
# print(DN_1)
assert P == P_1
assert D == D_1
assert DN == DN_1
assert V_in == V_in_1
assert V_out == V_out_1
