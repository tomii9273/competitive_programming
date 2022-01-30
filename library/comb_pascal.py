# modなし:
# O(le^2)、ただし桁数が膨大になるため、これにlog(le)がつくともいえる。
# le=1010 のとき、最大303桁の数が登場する。
# modあり:O(le^2)

le = 1010
# mod = 10**9 + 7

C = [[0] * le for i in range(le)]
for i in range(le):
    C[i][0] = 1
    # C[i][0] %= mod

for i in range(1, le):
    for j in range(1, le):
        C[i][j] = C[i-1][j-1] + C[i-1][j]
        # C[i][j] %= mod
