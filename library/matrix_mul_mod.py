import numpy as np

mod = 10**9 + 7

# 参考：https://atcoder.jp/contests/abc199/submissions/22086320

# numpy.array(int64)である行列AとBの積を、modで求める。modが10^9程度ならオーバーフローしない。
# 注意：PyPyでなくPythonで提出！！


def mat_mul(A, B, mod=mod):
    A1, A2 = A >> 15, A & (1 << 15) - 1
    B1, B2 = B >> 15, B & (1 << 15) - 1
    X = (A1 @ B1) % mod
    Y = (A2 @ B2) % mod
    Z = ((A1 + A2) @ (B1 + B2) - X - Y) % mod
    return ((X << 30) + (Z << 15) + Y) % mod
