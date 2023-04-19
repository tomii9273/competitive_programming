import sys


# sys.setrecursionlimit(10 ** 9)  # Codeforcesでは350000程度に
def input():
    return sys.stdin.readline().strip()


n = int(input())
C = [list(map(int, input().split())) for i in range(n - 1)]

for i in range(len(C)):  # 入力が 1-indexed の場合
    for j in range(2):
        C[i][j] -= 1


M = [[] for i in range(n)]
for i in range(n - 1):
    M[C[i][0]].append(C[i][1])
    M[C[i][1]].append(C[i][0])  # 有向グラフの場合は削除！！


P = [-1] * n  # iの親ノードの番号（最短路などの復元用）
D = [-1] * n  # 始点からiまでの最短距離（兼訪問フラグ）
DN = [-1] * n  # i以深のノード総数（i自身も含める）
V_in = []  # 入った順に頂点番号を記録
V_out = []  # 出た順に頂点番号を記録


def dfs(i, next_ind):
    if next_ind == len(M[i]):
        V_out.append(i)
        DN[i] = 1
        for x in M[i]:
            if P[x] == i:
                DN[i] += DN[x]
                print(i, x, DN[x], P[i])
        ST.pop()
    else:
        x = M[i][next_ind]
        if D[x] != -1:
            ST[-1] = (i, next_ind + 1)
        else:
            D[x] = D[i] + 1
            P[x] = i
            V_in.append(x)
            ST.append((x, 0))


s = 0  # 始点の番号
D[s] = 0
V_in.append(s)

ST = [(s, 0)]
while len(ST) > 0:
    dfs(*ST[-1])
