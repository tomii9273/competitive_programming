# ACLのmath.hppではなく https://qiita.com/drken/items/ae02240cd1f8edfc86fd のロジックをもとにした。

from math import gcd


# 拡張Euclidの互除法。ap + bq = gcd(a, b) となる p, q, d=gcd(a, b) を返す。
def extgcd(a, b):
    if b == 0:
        return 1, 0, a
    q, p, d = extgcd(b, a % b)
    q -= (a // b) * p
    return p, q, d


def inv_e(x, mod):  # x の mod での逆元(存在しない場合-1)を返す。素数などの制約無し。O(log(min(x, mod)))
    x %= mod
    if mod == 1 or gcd(x, mod) != 1:
        return -1
    ans, _, _ = extgcd(x, mod)
    return ans % mod


def crt(R, M):  # 中国剰余定理。Rは余り、Mは割る数の配列。不定なら(0,1)、不能なら(0,0)が返る。
    assert len(R) == len(M)
    r = 0
    m = 1
    for i in range(len(R)):
        p, _, d = extgcd(m, M[i])
        if (R[i] - r) % d != 0:
            return (0, 0)
        tmp = (R[i] - r) // d * p % (M[i] // d)
        r += m * tmp
        m *= M[i] // d
    return (r % m, m)
