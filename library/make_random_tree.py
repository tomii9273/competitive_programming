def make_random_tree(n, one_indexed=False):
    """n 頂点の木をランダムに作成し、辺のリストを返す。"""
    from random import randint, shuffle

    A = []
    for i in range(n - 1):
        A.append([randint(0, i), i + 1])
    B = [i for i in range(n)]
    shuffle(B)
    for i in range(n - 1):
        for j in range(2):
            A[i][j] = B[A[i][j]]
        shuffle(A[i])
    shuffle(A)
    if one_indexed:
        for i in range(len(A)):
            for j in range(2):
                A[i][j] += 1
    return A
