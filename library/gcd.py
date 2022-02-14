from math import gcd
# AtCoderのPython3.8.2やPyPy3(Python3.7.3)だとこちらがよい

# from fractions import gcd
# Python3.4.3やPyPy3(Python3.2.5)だとこのgcdが使える

# def gcd(x, y):
#     if x == 0 and y == 0:
#         return float("inf")
#     while x != 0 and y != 0:
#         x, y = max(x, y), min(x, y)
#         x %= y
#     return max(x, y)
# これは基本的には使わない


def lcm(x, y):
    return int((x * y) // gcd(x, y))


def gcd_list(A):
    if A == [0] * len(A):
        return float("inf")
    ans = A[0]
    for i in range(1, len(A)):
        if A[i] != 0:
            ans = gcd(ans, A[i])
    return ans


def lcm_list(A):
    ans = A[0]
    for i in range(1, len(A)):
        ans = lcm(ans, A[i])
    return ans
