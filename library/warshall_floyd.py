from scipy.sparse.csgraph import floyd_warshall

# for i in range(len(C)):  # 1-indexedの場合
#     for j in range(2):
#         C[i][j] -= 1

big = 10 ** 20  # 距離infを示す数(必要以上に大きくしない)

M = [[big] * n for i in range(n)]

for i in range(n):
    M[i][i] = 0

for i in range(len(C)):
    M[C[i][0]][C[i][1]] = C[i][2]  # 辺の重み付け
    M[C[i][1]][C[i][0]] = C[i][2]

# 基本的にscipyを使ってPythonで通した方が速い
M = floyd_warshall(M)


# 以下は上記のコードでできない場合

# for k in range(n):
#     for i in range(n):
#         for j in range(n):
#             M[i][j] = min(M[i][j], M[i][k] + M[k][j])

# print(M)
