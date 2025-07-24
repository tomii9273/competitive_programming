def two_points_to_line(x0, y0, x1, y1):
    """
    2 点 (x0, y0), (x1, y1) を通る直線を調べる。
    ただ 1 つの直線 ax + by + c = 0 に定まる ... (0, a, b, c) を返す。
    無数の直線がある (同一点) ... 直線 ax + by + c = 0 を 1 つとして、(1, a, b, c) を返す。
    """
    if x0 == x1 and y0 == y1:
        return 1, y0, -x0, 0
    else:
        return 0, y1 - y0, x0 - x1, x1 * y0 - x0 * y1


def two_lines_to_point(a0, b0, c0, a1, b1, c1):
    """
    2 直線 a0 x + b0 y = c0, a1 x + b1 y = c1 の共有点を調べる。
    ただ 1 つの共有点 (x, y) がある (交わる) ... (0, x, y) を返す。
    無数の共有点がある (同一直線) ... 点 (x, y) を共有点の 1 つとして、(1, x, y) を返す。(*)
    共有点がない (平行) ... (2, 0, 0) を返す。
    (*) 格子点である共有点がある場合は拡張 Euclid の互除法で求められる。
    """
    assert a0 != 0 or b0 != 0
    assert a1 != 0 or b1 != 0
    deno = a0 * b1 - a1 * b0
    if deno == 0:
        if a0 * c1 - a1 * c0 == 0:
            if b0 != 0:
                return 1, 0, -c0 / b0
            else:
                return 1, -c0 / a0, 0
        else:
            return 2, 0, 0
    return 0, (b0 * c1 - b1 * c0) / deno, (a1 * c0 - a0 * c1) / deno
