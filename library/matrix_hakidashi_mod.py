def inv(x, mod):  # x の mod での逆元を返す。modが素数で、xとmodが互いに素である必要あり。
    x %= mod
    if x == 2:
        return (mod + 1) // 2
    return pow(x, mod - 2, mod)


def det(C, mod):
    """
    正方行列 C の行列式を mod で求める。
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
            factor = C[j][i] * invf
            for k in range(i, n):
                C[j][k] -= factor * C[i][k]
                C[j][k] %= mod
    return ans
