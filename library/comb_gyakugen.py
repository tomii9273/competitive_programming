mod = 10**9 + 7
le = 3*10**5 + 3


def pow(x, y, zz=1):  # x**y の mod を返す。modは素数でなくてもよい。zzは(modの倍数)^0の値。
    x %= mod
    if x == 0 and y == 0:
        return zz % mod
    ans = 1
    while y > 0:
        if y % 2 == 1:
            ans = (ans * x) % mod
        x = (x**2) % mod
        y //= 2
    return ans % mod


def inv(x):  # x の mod での逆元を返す。modが素数で、xとmodが互いに素である必要あり。
    x %= mod
    if x == 2:
        return (mod + 1) // 2
    return pow(x, mod - 2)


M = [1]  # i!
mul = 1
for i in range(1, le):
    mul = (mul * i) % mod
    M.append(mul)

MI = [0] * (le-1) + [inv(M[le-1])]  # i!の逆元
for i in range(le-2, -1, -1):
    MI[i] = MI[i+1] * (i+1) % mod


def C(x, y):  # コンビネーション (組合せ, 二項係数)
    if y < 0 or y > x:
        return 0
    elif x >= le:  # O(min(y, x-y))
        y = min(y, x-y)
        ans = 1
        for i in range(x, x-y, -1):
            ans = (ans * i) % mod
        return (ans * MI[y]) % mod
    else:  # O(1)
        ans = M[x]
        ans = (ans * MI[y]) % mod
        return (ans * MI[x-y]) % mod


def H(x, y):  # 重複組合せ、x + y < le にすることに注意
    return C(x+y-1, y)


def P(x, y):  # パーミュテーション (順列)
    if y < 0 or y > x:
        return 0
    elif x >= le:  # O(min(y, x-y))
        y = min(y, x-y)
        ans = 1
        for i in range(x, x-y, -1):
            ans = (ans * i) % mod
        return ans % mod
    else:  # O(1)
        ans = M[x]
        return (ans * MI[x-y]) % mod
