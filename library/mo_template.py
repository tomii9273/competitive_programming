# ABC293-G を元にした、Mo's algorithm のテンプレート

import sys

sys.setrecursionlimit(10 ** 9)  # Codeforcesでは350000程度に


def input():
    return sys.stdin.readline().strip()


n, q = map(int, input().split())
A = list(map(int, input().split()))
Q = [list(map(int, input().split())) for _ in range(q)]
for i in range(q):
    for j in range(2):
        Q[i][j] -= 1

m = int((2 * 10 ** 5 + 10) ** 0.5) + 10

D = [[] for _ in range(m)]

for i in range(q):
    D[Q[i][0] // m].append([Q[i][0], Q[i][1], i])

for i in range(m):
    D[i].sort(reverse=(i % 2 == 1), key=lambda x: x[1])

# print(D)

now = 0
nowl = 0
nowr = -1
ANS = [-1] * q

DA = sorted(list(set(A)))
DB = {DA[i]: i for i in range(len(DA))}
for i in range(n):
    A[i] = DB[A[i]]

NOW = [0] * len(DA)


def diff(x):
    return ((x - 1) * (x - 2)) // 2


for i in range(m):
    for j in range(len(D[i])):
        l, r, ind = tuple(D[i][j])
        while l < nowl:
            nowl -= 1
            t = A[nowl]
            NOW[t] += 1
            now += diff(NOW[t])
        while l > nowl:
            t = A[nowl]
            now -= diff(NOW[t])
            NOW[t] -= 1
            nowl += 1
        while r < nowr:
            t = A[nowr]
            now -= diff(NOW[t])
            NOW[t] -= 1
            nowr -= 1
        while r > nowr:
            nowr += 1
            t = A[nowr]
            NOW[t] += 1
            now += diff(NOW[t])
        ANS[ind] = now

for ans in ANS:
    print(ans)
