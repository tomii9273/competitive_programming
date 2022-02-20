# 多角形 P_0 P_1 ... P_(n-1) の面積を返す。頂点はこの順番でなければならない。
# 凹でも可。必ず0.5刻みになるが、誤差対策で整数にしたい場合はx2=True。
def area_of_polygon(Ps, is_x2=False):
    ans = 0
    for i in range(len(Ps)):
        ans += (Ps[i][0] - Ps[i - 1][0]) * (Ps[i][1] + Ps[i - 1][1])
    ans = abs(ans)
    if is_x2:
        return ans
    return ans / 2
