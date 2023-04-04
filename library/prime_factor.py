from math import gcd

# 参考
# https://nyaannyaan.github.io/library/prime/fast-factorize.hpp.html
# https://qiita.com/Kiri8128/items/eca965fe86ea5f4cbb98#fnref1
# https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
# https://ja.wikipedia.org/wiki/%E3%83%9D%E3%83%A9%E3%83%BC%E3%83%89%E3%83%BB%E3%83%AD%E3%83%BC%E7%B4%A0%E5%9B%A0%E6%95%B0%E5%88%86%E8%A7%A3%E6%B3%95
# https://manabitimes.jp/math/1192

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]


def is_prime_miller_test(n: int) -> bool:
    """
    n が素数かどうかを Miller test で判定する。
    a として 37 までの素数を試せば、10^23 以下の数について正確に判定できる。
    時間計算量: O((log n)^2 * len(PRIMES))
    参考: https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    """
    if n == 2:
        return True
    if n == 1 or n % 2 == 0:
        return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in PRIMES:
        if a > n - 2:
            break
        x = pow(a, d, n)
        for _ in range(s):
            y = pow(x, 2, n)
            if y == 1 and x != 1 and x != n - 1:
                return False
            x = y
        if y != 1:
            return False
    return True


def ro(n: int) -> int:
    """
    ポラード・ロー法で n の約数のうちの1つを求める。
    時間計算量 (概算値): O(n^(1/4) log n)
    以下の場合、失敗することが多いので注意。
    - n が素数
    - n が小さい (100 未満くらいの) 素因数をもつ
    参考: https://qiita.com/Kiri8128/items/eca965fe86ea5f4cbb98#fnref1, https://manabitimes.jp/math/1192
    """
    assert n > 100

    for c in range(1, 100):

        def f(x):
            return (pow(x, 2, n) + c) % n

        x = 0
        y = 0
        g = 1
        while g == 1:
            x = f(x)
            y = f(f(y))
            g = gcd((x - y) % n, n)

        if n != g:
            break

    return g


def get_factors(n: int) -> dict:
    """
    n の素因数の dict を得る。
    時間計算量 (概算値): O(n^(1/4) log n)
    """
    ans = {}
    if n == 0 or n == 1:
        return ans
    if is_prime_miller_test(n):
        return {n: 1}
    for i in range(2, 100):
        while n % i == 0:
            n //= i
            if i in ans:
                ans[i] += 1
            else:
                ans[i] = 1
    if n > 100:
        ST = [n]
        while ST:
            t = ST.pop()
            if is_prime_miller_test(t):
                if t in ans:
                    ans[t] += 1
                else:
                    ans[t] = 1
            else:
                t0 = ro(t)
                t1 = t // t0
                ST += [t0, t1]
    return ans


def get_factors_naive(n: int) -> dict:
    """
    n の素因数の dict を得る。(試し割り法、テスト用)
    時間計算量: O(n^(1/2))
    """
    ans = {}
    if n == 0 or n == 1:
        return ans
    for i in range(2, int(n ** 0.5) + 1):
        while n % i == 0:
            n //= i
            if i in ans:
                ans[i] += 1
            else:
                ans[i] = 1
    if n != 1:
        if n in ans:
            ans[n] += 1
        else:
            ans[n] = 1
    return ans


# 以下テスト

for i in range(10 ** 5):
    # print(i)
    assert get_factors(i) == get_factors_naive(i), (get_factors(i), get_factors_naive(i))

for i in range(10 ** 9, 10 ** 9 + 10 ** 4):
    # print(i, get_factors_naive(i))
    if i % (10 ** 2) == 0:
        print(i)
    assert get_factors(i) == get_factors_naive(i), (get_factors(i), get_factors_naive(i))

print(get_factors((2 ** 19 - 1) * (2 ** 31 - 1)))


le = 10 ** 5
is_prime = [True] * le
is_prime[0] = False
is_prime[1] = False
for i in range(2, le):
    if is_prime[i]:
        for j in range(i * 2, le, i):
            is_prime[j] = False

for i in range(le):
    assert is_prime[i] == is_prime_miller_test(i), (i, is_prime[i], is_prime_miller_test(i))


# 桁数が十分大きい数
assert not is_prime_miller_test(10 ** 18)
assert is_prime_miller_test(67_280_421_310_721)

# メルセンヌ数
assert not is_prime_miller_test(2 ** 59 - 1)
assert is_prime_miller_test(2 ** 61 - 1)

# 擬素数
assert not is_prime_miller_test(1194649)  # 1093^2
assert not is_prime_miller_test(12327121)  # 3511^2
assert not is_prime_miller_test((2 ** 19 - 1) * (2 ** 31 - 1))
