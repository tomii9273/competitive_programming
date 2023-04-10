def inv(x, mod):
    """x の mod での逆元を返す。modが素数で、xとmodが互いに素である必要あり。"""
    x %= mod
    if x == 2:
        return (mod + 1) // 2
    return pow(x, mod - 2, mod)


def det(C, mod):
    """
    正方行列 C の行列式を mod (素数) で求める。
    掃き出し法 (ガウス・ジョルダンの消去法) を用いて (行基本変形を繰り返して) 、上三角行列にし、対角成分の積を求める。
    時間計算量: O(N^3) (C を N × N 正方行列としたとき)
    """
    n = len(C)
    ans = 1

    for i in range(n):
        ind = -1
        for j in range(i, n):
            if C[j][i] != 0:
                ind = j
                break
        if ind == -1:
            ans = 0
            break
        elif ind != i:
            ans *= -1
            ans %= mod
        C[i], C[ind] = C[ind], C[i]
        invf = inv(C[i][i], mod)
        ans *= C[i][i]
        ans %= mod

        for j in range(i + 1, n):
            factor = C[j][i] * invf % mod
            for k in range(i, n):
                C[j][k] -= factor * C[i][k]
                C[j][k] %= mod
    return ans


def inv_matrix(C, mod):
    """
    正方行列 C の逆行列を mod (素数) で求める。存在しない場合は -1 を返す。
    掃き出し法 (ガウス・ジョルダンの消去法) を用いて (行基本変形を繰り返して) 、N × 2N 行列 (C I) を (I C^-1) に変形する (I は単位行列) 。
    時間計算量: O(N^3) (C を N × N 正方行列としたとき)
    """
    n = len(C)

    # 横幅を拡張
    for i in range(n):
        C[i] += [0] * n
        C[i][n + i] = 1

    for i in range(n):
        ind = -1
        for j in range(i, n):
            if C[j][i] != 0:
                ind = j
                break
        if ind == -1:
            return -1

        C[i], C[ind] = C[ind], C[i]
        invf = inv(C[i][i], mod)
        for j in range(i, 2 * n):
            C[i][j] *= invf
            C[i][j] %= mod
        # assert C[i][i] == 1

        for j in range(n):
            if j != i:
                factor = C[j][i]
                for k in range(i, n * 2):
                    C[j][k] -= C[i][k] * factor
                    C[j][k] %= mod

    return [C[i][n:] for i in range(n)]
