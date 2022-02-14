def sqrt_floor(x):
    """a <= sqrt(x) となる最大の a (>= 0) を返す"""
    a = int(x**0.5)
    ans = a-3
    for i in range(a-1, a+2):
        if i >= 0 and i**2 <= x:
            ans = max(i, ans)
    return ans


def sqrt_ceil(x):
    """sqrt(x) <= a となる最小の a (>= 0) を返す"""
    a = int(x**0.5)
    ans = a+3
    for i in range(a-1, a+2):
        if i >= 0 and x <= i**2:
            ans = min(i, ans)
    return ans


big = 1234567891

print(sqrt_floor(big**2 - 1))
print(sqrt_floor(big**2))
print(sqrt_floor(big**2 + 1))

print(sqrt_ceil(big**2 - 1))
print(sqrt_ceil(big**2))
print(sqrt_ceil(big**2 + 1))
