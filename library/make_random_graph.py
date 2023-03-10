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


def make_random_graph(n, r=0.5, one_indexed=False):
    """
    n 頂点の単純無向グラフをランダムに作成し、辺のリストを返す。
    非連結である可能性あり。
    r は辺を張る (大体の) 割合。
    計算量: O(n^2)
    """
    from random import random, shuffle

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random() < r:
                edges.append([i, j])
                shuffle(edges[-1])
    shuffle(edges)
    if one_indexed:
        for i in range(len(edges)):
            for j in range(2):
                edges[i][j] += 1
    return edges
