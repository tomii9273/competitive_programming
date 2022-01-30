# INはその頂点を指している辺の本数のリスト

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
