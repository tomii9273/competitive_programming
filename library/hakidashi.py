import numpy as np


# ※ACを確認していない（https://atcoder.jp/contests/zone2021/tasks/zone2021_f で使おうとしたがTLE）

# 行列M(n行m列とする)に対して掃き出し法(Gauss-Jordanの消去法)(行基本変形で)
# を行い、ランクrや基底を求める。
# 掃き出し後の行列M'とランクを返す。
# r=nのとき、M'[:r, :r]はR^r空間の基底行列となる。
# そうでない場合も含め、
# ・M[ZR, :]およびM'[:r, :]の行ベクトルたちは線型独立であり、元の行列の行ベクトルの線型結合で表せるような空間の基底となっている。
# ・M[:, ZC]の列ベクトルたちは線型独立であり、元の行列の列ベクトルの線型結合で表せるような空間の基底となっている。
# ・M[ZR, ZC]はR^r空間の基底行列である。(未証明だが、テストコードで確認)
# O(n^2 m)
def hakidashi(M, t=False, eps=1e-9):
    # 必ずPythonで提出！！！
    if M is not np.ndarray:
        M = np.array(M, dtype="float64")
    if t:
        M = M.T
    n, m = M.shape
    ZR = np.zeros(n, dtype="bool")
    ZC = np.ones(m, dtype="bool")
    ZRi = [i for i in range(n)]
    indr = 0
    for i in range(m):
        ind0 = np.argmax(M[indr:, i]) + indr
        ind1 = np.argmin(M[indr:, i]) + indr
        if abs(M[ind0, i]) >= abs(M[ind1, i]):
            ind = ind0
        else:
            ind = ind1
        if abs(M[ind, i]) < eps:
            ZC[i] = 0
            continue
        ZR[ZRi[ind]] = 1
        if indr != ind:
            M[[indr, ind]] = M[[ind, indr]]
            ZRi[indr], ZRi[ind] = ZRi[ind], ZRi[indr]
        M[indr] /= M[indr, i]
        for j in range(indr + 1, n):
            M[j] -= M[indr] * M[j, i]
        indr += 1
        if indr == n:
            ZC[i + 1 :] = 0
            break
    r = sum(ZC)
    return M, r, ZR, ZC


# テストコード
for _ in range(1000):
    M = np.random.randint(-2, 2, (2, 4))
    r0 = np.linalg.matrix_rank(M)
    MD, r, ZR, ZC = hakidashi(M, 0)
    if (
        r != r0
        or r != sum(ZR)
        or r != sum(ZC)
        or (M[ZR][:, ZC].shape != (0, 0) and np.linalg.matrix_rank(M[ZR][:, ZC]) != r)
    ):
        print(M, np.linalg.matrix_rank(M), r0, MD, r, ZR, ZC)
        break
