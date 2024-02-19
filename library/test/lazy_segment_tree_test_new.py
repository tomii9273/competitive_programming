import sys

sys.path.append("../")
from library.lazy_segment_tree import LazySegtree

inf = float("inf")
length = 10
seg = LazySegtree(length)

# update の確認
seg.update(0, 1)
seg.update(2, -1)
expected = [1, inf, -1, inf, inf, inf, inf, inf, inf, inf]

assert [seg[i] for i in range(length)] == expected

# prod の確認
for le in range(length):
    for ri in range(le, length):
        if le == ri:
            assert seg.prod(le, ri) == inf
        else:
            assert seg.prod(le, ri) == min(expected[le:ri])

for i in range(length):
    if seg[i] == inf:
        seg.update(i, 10)

expected = [1, 10, -1, 10, 10, 10, 10, 10, 10, 10]

assert [seg[i] for i in range(length)] == expected

# apply の確認
seg.apply(0, 6, 10)
seg.apply(4, 9, -10)
seg.apply(3, 3, -10000)
seg.update(5, -100)
expected = [11, 20, 9, 20, 10, -100, 0, 0, 0, 10]

assert [seg[i] for i in range(length)] == expected


for le in range(length):
    for ri in range(le, length):
        if le == ri:
            assert seg.prod(le, ri) == inf
        else:
            assert seg.prod(le, ri) == min(expected[le:ri])
