import sys
# sys.setrecursionlimit(10 ** 9)  # Codeforcesでは350000程度に
def input(): return sys.stdin.readline().strip()


# 文字列s,tの中に適切に空白文字を挿入して長さを揃える (=ペアワイズアラインメントを行う) ことで、
# s,t間の類似度を最大化する。
# 類似度の最大値およびそのときの挿入後のs,tを返す。
# DPで行う。計算量は O(|s||t|) 。

s = input()
t = input()


# パラメータここから

big = 10**5  # 途中で取り得るスコアの最小値の絶対値より大きく
sp = "-"  # 空白文字
pena_sp = -5  # 空白文字との類似度


def diff(i, j):  # 類似度を定義する関数
    if s[i] == t[j]:
        return 1
    return -3


# パラメータここまで


n = len(s)
m = len(t)


D = [[-big] * (m+1) for i in range(n+1)]
E = [[-1] * (m+1) for i in range(n+1)]

D[0][0] = 0

for i in range(n+1):
    for j in range(m+1):
        if i == 0 and j == 0:
            continue
        K = []
        if j > 0:
            K.append([D[i][j-1] + pena_sp, 0])
        if i > 0:
            K.append([D[i-1][j] + pena_sp, 1])
        if j > 0 and i > 0:
            K.append([D[i-1][j-1] + diff(i-1, j-1), 2])
        K.sort(reverse=True)
        D[i][j] = K[0][0]
        E[i][j] = K[0][1]


print(D[-1][-1])  # 最大スコア


# 以下、挿入後のs,tを復元する場合

sind = n
tind = m
SANS = []
TANS = []

while True:
    e = E[sind][tind]
    if e == 0:
        tind -= 1
        SANS.append("-")
        TANS.append(t[tind])
    elif e == 1:
        sind -= 1
        SANS.append(s[sind])
        TANS.append("-")
    elif e == 2:
        sind -= 1
        tind -= 1
        SANS.append(s[sind])
        TANS.append(t[tind])
    if e == -1:
        break

s_ans = "".join(SANS[::-1])
t_ans = "".join(TANS[::-1])

# print(s_ans)  # 文字列s
# print(t_ans)  # 文字列t
