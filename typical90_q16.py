# A,B,Cの最大値をM、答えの上限をUとすると、O(min(U, N/M) log M) のはず

n = int(input())
L = list(map(int, input().split()))
L.sort(reverse=True)
a, b, c = L[0], L[1], L[2]


# 拡張Euclidの互除法。ap + bq = gcd(a, b) となる p, q, d=gcd(a, b) を返す。
def extgcd(a, b):
    if b == 0:
        return 1, 0, a
    q, p, d = extgcd(b, a % b)
    q -= (a // b) * p
    return p, q, d


# 中国剰余定理。Rは余り、Mは割る数の配列。不定なら(0,1)、不能なら(0,0)が返る。
def crt(R, M):
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


ans = 10**4
for i in range(min(n//a + 1, 10**4)):
    nn = n - a*i
    ans_now = i
    re, q = crt([nn % b, 0], [b, c])
    if q != 0 and nn - re >= 0:
        ans_now += re // c + (nn - re) // b
        ans = min(ans, ans_now)

print(ans)
