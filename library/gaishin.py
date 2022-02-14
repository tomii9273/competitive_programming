# 3点の座標から、その外接円の中心の座標を返す。
# 3点が一直線上にある場合は、端の2点を結んだ線分を直径とする円の中心の座標を返す。
# epsは一直線上とみなす閾値。
def gaishin3(xa, ya, xb, yb, xc, yc, eps=1e-8):
    a = ((xb-xc) ** 2 + (yb-yc) ** 2) ** 0.5  # 頂点Aの対辺の長さ
    b = ((xa-xc) ** 2 + (ya-yc) ** 2) ** 0.5  # 頂点Bの対辺の長さ
    c = ((xb-xa) ** 2 + (yb-ya) ** 2) ** 0.5  # 頂点Cの対辺の長さ
    # print("abc",a,b,c)
    ca = (b**2 + c**2 - a**2) / (2*b*c)  # cos A
    cb = (a**2 + c**2 - b**2) / (a*2*c)  # cos B
    cc = (a**2 + b**2 - c**2) / (a*b*2)  # cos C
    sa2 = 2 * ca * (max(0, 1-ca**2) ** 0.5)  # sin 2A
    sb2 = 2 * cb * (max(0, 1-cb**2) ** 0.5)  # sin 2B
    sc2 = 2 * cc * (max(0, 1-cc**2) ** 0.5)  # sin 2C
    if sa2 + sb2 + sc2 < eps:  # 一直線上の場合
        x = (max(xa, xb, xc) - min(xa, xb, xc)) / 2
        y = (max(ya, yb, yc) - min(ya, yb, yc)) / 2
    else:
        x = (sa2*xa + sb2*xb + sc2*xc) / (sa2 + sb2 + sc2)  # こういう公式がある
        y = (sa2*ya + sb2*yb + sc2*yc) / (sa2 + sb2 + sc2)
    return [x, y]


def gaishin2(xa, ya, xb, yb):  # 2点の座標から、それらを結んだ線分を直径とする円の中心の座標(中点の座標)を返す。
    x = (xa + xb) / 2
    y = (ya + yb) / 2
    return [x, y]
