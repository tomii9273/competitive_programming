def sqrt_floor(x):
    """
    a <= sqrt(x) となる最大の a (>= 0) を返す
    x が 10 ** 14 以上になるなら、int(x ** 0.5) ではなくこの関数を使用するのが安全
    """
    a = int(x ** 0.5)
    ans = a - 3
    for i in range(a - 1, a + 2):
        if i >= 0 and i ** 2 <= x:
            ans = max(i, ans)
    return ans


def sqrt_ceil(x):
    """sqrt(x) <= a となる最小の a (>= 0) を返す"""
    a = int(x ** 0.5)
    ans = a + 3
    for i in range(a - 1, a + 2):
        if i >= 0 and x <= i ** 2:
            ans = min(i, ans)
    return ans


# 誤差がないことのテスト

big = 1234567891

print(sqrt_floor(big ** 2 - 1))
print(sqrt_floor(big ** 2))
print(sqrt_floor(big ** 2 + 1))

print(sqrt_ceil(big ** 2 - 1))
print(sqrt_ceil(big ** 2))
print(sqrt_ceil(big ** 2 + 1))


# int(i ** 0.5) の誤差のテスト

length = 1000

for i in range(10 ** 7, 10 ** 7 + length):
    for j in range(i ** 2 - 2, i ** 2 + 2):
        if sqrt_floor(j) != int(j ** 0.5):
            print(i, j)  # まだ誤差は出ない

for i in range(10 ** 8, 10 ** 8 + length):
    for j in range(i ** 2 - 2, i ** 2 + 2):
        if sqrt_floor(j) != int(j ** 0.5):
            print(i, j)  # 誤差が出始める
