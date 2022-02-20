# 小さいmod (9桁とかにならないもの、そのmodの倍数を乗除で扱いうるようなもの) での二項係数など。
# modは素数である必要がある。

mod = 3
le = 3 * 10 ** 5 + 3


def pow(x, y):  # x**y の mod を返す。modは素数でなくてもよい。
    x %= mod
    ans = 1
    while y > 0:
        if y % 2 == 1:
            ans = (ans * x) % mod
        x = (x ** 2) % mod
        y //= 2
    return ans % mod


def inv(x):  # x の mod での逆元を返す。modが素数で、xとmodが互いに素である必要あり。
    x %= mod
    if x == 2:
        return (mod + 1) // 2
    return pow(x, mod - 2)


def int_to_pair(x):  # x を (modで割れる回数, x % mod) で表す。
    if x == 0:
        return (0, 0)
    x0 = 0
    while x % mod == 0:
        x //= mod
        x0 += 1
    return (x0, x % mod)


def pair_to_int(x):  # (modで割れる回数, x % mod) を整数に戻す。1回でも割れるなら0。
    return 0 if x[0] > 0 else x[1]


def mul_pair(x, y):  # x * y
    return (x[0] + y[0], (x[1] * y[1]) % mod)


def div_pair(x, y):  # x / y
    return (x[0] - y[0], (x[1] * inv(y[1])) % mod)


PA = [int_to_pair(i) for i in range(le)]

M = [(0, 1)]  # i!
for i in range(1, le):
    M.append(mul_pair(M[-1], PA[i]))

MI = [(0, 0)] * (le - 1) + [div_pair(PA[1], M[le - 1])]  # i!の逆元
for i in range(le - 2, -1, -1):
    MI[i] = mul_pair(MI[i + 1], PA[i + 1])


def C(x, y):  # コンビネーション (組合せ, 二項係数)
    if y < 0 or y > x:
        return 0
    elif x >= le:  # O(min(y, x-y))
        y = min(y, x - y)
        ans = PA[1]
        for i in range(x, x - y, -1):
            ans = mul_pair(ans, int_to_pair(i))
        return pair_to_int(mul_pair(ans, MI[y]))
    else:  # O(1)
        return pair_to_int(mul_pair(mul_pair(M[x], MI[y]), MI[x - y]))


def H(x, y):  # 重複組合せ、x + y < le にすることに注意
    return C(x + y - 1, y)


def P(x, y):  # パーミュテーション (順列)
    if y < 0 or y > x:
        return 0
    elif x >= le:  # O(min(y, x-y))
        y = min(y, x - y)
        ans = PA[1]
        for i in range(x, x - y, -1):
            ans = mul_pair(ans, int_to_pair(i))
        return pair_to_int(ans)
    else:  # O(1)
        return pair_to_int(mul_pair(M[x], MI[x - y]))
