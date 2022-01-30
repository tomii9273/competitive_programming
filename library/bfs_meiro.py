h, w = map(int, input().split())
si, sj = map(int, input().split())
gi, gj = map(int, input().split())
C = [input() for i in range(h)]

si -= 1
sj -= 1
gi -= 1
gj -= 1

V = [[-1] * w for i in range(h)]
D = [[-1, 0], [1, 0], [0, -1], [0, 1]]

Q = [[si, sj, 0]]
s = 0
V[si][sj] = 0
while s < len(Q):
    i = Q[s][0]
    j = Q[s][1]
    d = Q[s][2]
    for t in D:
        di = t[0]
        dj = t[1]
        if 0 <= i+di < h and 0 <= j+dj < w \
                and V[i+di][j+dj] == -1 and C[i+di][j+dj] == ".":
            V[i+di][j+dj] = d+1
            Q.append([i+di, j+dj, d+1])
    s += 1

print(V[gi][gj])
