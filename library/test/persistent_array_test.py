import sys
from random import choice, randint

sys.path.append("../")
from library.persistent_array import Node, PersistentArray

# from library.persistent_array import PersistentArrayBit as PersistentArray

base_ar = [1, 2, 3, 4, 5, 6, 17, 18, 19, 20]


ar = PersistentArray(10, 0, base_ar, 2)

# for i in range(len(ar.tree)):
#     print(i, ar.tree[i].val, ar.tree[i].lch, ar.tree[i].rch)
# print(ar.ver_list)

assert ar.size == 10
assert ar.k == 4
assert ar.size2 == 16

assert ar.get_all(2) == base_ar + [0] * 6, (ar.get_all(2), base_ar + [0] * 6)
assert [ar.get(2, i) for i in range(10)] == base_ar

ar.update(2, 3, 3, 100)

base_ar = [1, 2, 3, 100, 5, 6, 17, 18, 19, 20]
assert ar.get_all(3) == base_ar + [0] * 6, (ar.get_all(3), base_ar + [0] * 6)
assert [ar.get(3, i) for i in range(10)] == base_ar

ar.update(3, 4, 4, 1000)

base_ar = [1, 2, 3, 100, 1000, 6, 17, 18, 19, 20]
assert ar.get_all(4) == base_ar + [0] * 6, (ar.get_all(4), base_ar + [0] * 6)
assert [ar.get(4, i) for i in range(10)] == base_ar

ar.update(2, 5, 0, -1)

base_ar = [-1, 2, 3, 4, 5, 6, 17, 18, 19, 20]
assert ar.get_all(5) == base_ar + [0] * 6, (ar.get_all(5), base_ar + [0] * 6)
assert [ar.get(5, i) for i in range(10)] == base_ar


# ランダムテスト

L = [[] for _ in range(30)]

base_ar = list(range(20))
ar = PersistentArray(20, 1, base_ar, 15)
base_ar += [1] * 12
L[15] = base_ar[:]
all_vers = set(range(30))
exist_vers = set([15])


for _ in range(29):
    t_new = choice(list(all_vers - exist_vers))
    t_old = choice(list(exist_vers))
    i = randint(0, 31)
    v = randint(-100, 100)
    # print("update", t_old, t_new, i, v)
    ar.update(t_old, t_new, i, v)
    L[t_new] = L[t_old][:]
    L[t_new][i] = v
    exist_vers.add(t_new)
    assert ar.get_all(t_new) == L[t_new], (ar.get_all(t_new), L[t_new])
    assert [ar.get(t_new, i) for i in range(32)] == L[t_new]
