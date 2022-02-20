class Bit:
    def __init__(self, n):
        self.size = n
        self.tree = [0] * (n + 1)

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s

    def add(self, i, x):
        while i <= self.size:
            self.tree[i] += x
            i += i & -i


def print_bit(B):
    n = B.size
    ANS = []
    for i in range(n):
        ANS.append(B.sum(i + 1) - B.sum(i))
    print(*ANS)


ppp = [3, 10, 1, 8, 5]
bit = Bit(16)
ans = 0

for i, p in enumerate(ppp):
    bit.add(p, 1)
    ans += i + 1 - bit.sum(p)

print(ans)
