from collections import deque
n = int(input())
C = [list(map(int, input().split())) for i in range(n-1)]  # 木でない場合は変える

for i in range(len(C)):  # 入力が 1-indexed の場合
    for j in range(2):
        C[i][j] -= 1


M = [[] for i in range(n)]
for i in range(len(C)):
    M[C[i][0]].append((C[i][1], C[i][2]))
    M[C[i][1]].append((C[i][0], C[i][2]))  # 有向グラフの場合は削除！！
    assert C[i][2] == 0 or C[i][2] == 1

for i in range(n):
    M[i] = tuple(M[i])
M = tuple(M)  # しない方が速い場合もある


s = 0  # 始点の番号

D = [-1] * n  # 始点からiまでの最短距離
Q = deque()  # 両端キュー

Q.append((s, 0))
while len(Q) > 0:
    i, d = Q.popleft()
    if D[i] == -1:
        D[i] = d
        for j, dd in M[i]:
            if dd == 0:
                if D[j] == -1:
                    Q.appendleft((j, d+dd))
            else:
                if D[j] == -1:
                    Q.append((j, d+dd))
