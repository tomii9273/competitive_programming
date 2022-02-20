# 三角形 P_0 P_1 P_2 の面積を返す。必ず0.5刻みになるが、誤差対策で整数にしたい場合はx2=True。
def area_of_triangle(P0, P1, P2, is_x2=False):
    # print("call tr", x2)
    x0, y0, x1, y1, x2, y2 = P0[0], P0[1], P1[0], P1[1], P2[0], P2[1]
    xa, ya, xb, yb = x1 - x0, y1 - y0, x2 - x0, y2 - y0
    ans = abs(xa * yb - xb * ya)
    if is_x2:
        return ans
    return ans / 2


# 多角形 P_0 P_1 ... P_(n-1) の面積を、area_of_triangleを元に返す。頂点はこの順番でなければならない。
# 凹でも可。必ず0.5刻みになるが、誤差対策で整数にしたい場合はx2=True。
def area_of_polygon_tr(Ps, is_x2=False):
    ans = 0
    for i in range(len(Ps) - 2):
        ans += area_of_triangle(Ps[0], Ps[i + 1], Ps[i + 2], is_x2=True)
    if is_x2:
        return ans
    return ans / 2
