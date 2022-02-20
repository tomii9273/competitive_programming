# 頂点の集合Pから、凸包を返す。3点以上の場合、多角形となる。
# 順序は、ソートで最小となる頂点から反時計回り。180度の角は除かれる。
def make_convex_hull(P):
    P.sort()
    n = len(P)
    S = [[], []]  # 下側凸包、上側凸包
    for i in range(2):
        for j in range(n):
            while len(S[i]) >= 2:
                x0 = S[i][-1][0] - S[i][-2][0]
                y0 = S[i][-1][1] - S[i][-2][1]
                x1 = P[j][0] - S[i][-1][0]
                y1 = P[j][1] - S[i][-1][1]
                cp = x0 * y1 - x1 * y0
                if (i == 0 and cp < 0) or (i == 1 and cp > 0):
                    S[i].pop()
                else:
                    break
            S[i].append(P[j][:])
    for j in range(len(S[1]) - 2, 0, -1):
        S[0].append(S[1][j][:])
    return S[0]
