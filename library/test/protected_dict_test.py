import sys

sys.path.append("../")
from library.protected_dict import ProtectedDict

D = ProtectedDict()

D[0] = 1
D[1] = 2

assert D[0] == 1
assert D[1] == 2
assert 0 in D
assert 1 in D
assert 2 not in D

D[0] = 3
assert D[0] == 3

del D[0]
assert 0 not in D

D[0] = 1
assert D.keys() == {0, 1}
assert D.values() == {1, 2}
assert D.items() == {(0, 1), (1, 2)}
