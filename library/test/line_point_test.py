import math
import sys

sys.path.append("../")

from library.line_point import two_lines_to_point, two_points_to_line


def isclose(a, b):
    return math.isclose(a, b, rel_tol=1e-09, abs_tol=1e-09)


t, a, b, c = two_points_to_line(1, 2, 3, 4)
assert t == 0
assert 1 * a + 2 * b + c == 0
assert 3 * a + 4 * b + c == 0


t, a, b, c = two_points_to_line(-1, 2, 30, -45)
assert t == 0
assert -1 * a + 2 * b + c == 0
assert 30 * a - 45 * b + c == 0

# 同一点
t, a, b, c = two_points_to_line(1, 2, 1, 2)
assert t == 1
assert 1 * a + 2 * b + c == 0


# 交わる、整数解
t, x, y = two_lines_to_point(1, 2, 3, 2, 1, 6)
assert t == 0
assert isclose(x, -3)
assert isclose(y, 0)
assert isclose(1 * x + 2 * y + 3, 0)
assert isclose(2 * x + 1 * y + 6, 0)

# 交わる、非整数解
t, x, y = two_lines_to_point(10.1, 2.9, 3.2, -0.3, -1.2, 6.8)
assert t == 0
assert isclose(10.1 * x + 2.9 * y + 3.2, 0)
assert isclose(-0.3 * x - 1.2 * y + 6.8, 0)


# 同一直線、b0 != 0
t, x, y = two_lines_to_point(1, 2, 3, 2, 4, 6)
assert t == 1
assert isclose(1 * x + 2 * y + 3, 0)
assert isclose(2 * x + 4 * y + 6, 0)

# 同一直線、b0 == 0
t, x, y = two_lines_to_point(1, 0, 3, 2, 0, 6)
assert t == 1
assert isclose(1 * x + 0 * y + 3, 0)
assert isclose(2 * x + 0 * y + 6, 0)

# 平行
t, x, y = two_lines_to_point(1, 2, 3, 2, 4, 5)
assert t == 2
