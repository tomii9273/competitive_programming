n, m = map(int, input().split())
C = [list(map(int, input().split())) for _ in range(m)]
for i in range(len(C)):  # 入力が 1-indexed の場合
    for j in range(2):
        C[i][j] -= 1


M = [[] for i in range(n)]
IN = [0] * n  # その頂点を指している辺の本数のリスト

for i in range(len(C)):
    M[C[i][0]].append(C[i][1])
    IN[C[i][1]] += 1


# A, 順番の制約なし、O(n + m)

S = []
s = 0

for i in range(n):
    if IN[i] == 0:
        S.append(i)

while s < len(S):
    for x in M[S[s]]:
        IN[x] -= 1
        if IN[x] == 0:
            S.append(x)
    s += 1

print(*S)

# B, 辞書順に並べる、O(n log n + m)

from heapq import heappop, heappush

Q = []

for i in range(n):
    if IN[i] == 0:
        heappush(Q, i)

ANS = []

while Q:
    i = heappop(Q)
    ANS.append(i)
    for x in M[i]:
        IN[x] -= 1
        if IN[x] == 0:
            heappush(Q, x)

print(*[i + 1 for i in ANS])
