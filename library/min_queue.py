class MinQueue:
    """右への追加・左からの削除・最小値の取得を O(1) で行えるキュー"""

    def __init__(self):
        self.q = []
        self.minq = []
        self.q_ind = 0
        self.minq_ind = 0

    def __len__(self):
        return len(self.q) - self.q_ind

    def push(self, x):
        while self.minq and self.minq[-1] > x:
            self.minq.pop()
            self.minq_ind = min(self.minq_ind, len(self.minq))
        self.minq.append(x)
        self.q.append(x)

    def pop(self):
        assert self.minq_ind < len(self.minq)
        if self.q[self.q_ind] == self.minq[self.minq_ind]:
            self.minq_ind += 1
        self.q_ind += 1

    def get_min(self):
        return self.minq[self.minq_ind]

    def print(self):
        print("q:", self.q[self.q_ind :])
        print("minq:", self.minq[self.minq_ind :])
