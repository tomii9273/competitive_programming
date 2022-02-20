# n頂点の木をランダムに作成し、辺のリスト(1-indexed)を返す。
def make_random_tree(n):
    from random import randint, shuffle

    A = []
    for i in range(n - 1):
        A.append([randint(1, i + 1), i + 2])
    B = [i for i in range(n)]
    shuffle(B)
    for i in range(n - 1):
        for j in range(2):
            A[i][j] = B[A[i][j] - 1] + 1
        shuffle(A[i])
    shuffle(A)
    return A
