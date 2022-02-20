# 参考: https://japlj.hatenadiary.org/entry/20090714/1247583495


# !注意! scc.py（強連結成分分解）のコピペがこのclassの前に必要！
class twosat:  # 2-SAT問題を解く
    def __init__(self, n):  # n変数の2-SATを作成
        self.n = n
        self.S = scc(2 * n)
        self.ANS = [True] * n

    def add_clause(self, i, f, j, g):
        # (x_i == f) or (x_j == g) (f,gはbool値) というクローズをandする
        fb = (int(f) + 1) % 2
        gb = (int(g) + 1) % 2
        self.S.add_edge(2 * i + fb, 2 * j + g)
        self.S.add_edge(2 * j + gb, 2 * i + f)

    def satisfiable(self):  # 条件を満たす割当があればTrue（解の構成もする）
        n = self.n
        sl = self.S.scc_list()
        A = [-1] * (2 * n)
        for i in range(len(sl)):
            for j in range(len(sl[i])):
                A[sl[i][j]] = i

        for i in range(n):
            if A[2 * i] == A[2 * i + 1]:
                return False
            self.ANS[i] = A[2 * i] < A[2 * i + 1]
        return True

    def answer(self):  # 解を返す（satisfiableを呼んだ後に）
        return self.ANS
