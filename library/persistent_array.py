# PersistentArray はサイズが 5 * 10^5 程度以上になると MLE の可能性があるので、基本的に PersistentArrayBit の方を使う。


class PersistentArrayBit:
    """
    永続配列 (完全二分木)。O(log n) で各種操作が可能。
    高速化・メモリ節約のため、Node クラスを整数で代用し、下から 30 ビットを右の子ノードの index、
    その上の 30 ビットを左の子ノードの index、その上のビットを値として扱っている。
    そのため、サイズは 2^30 以下、入れるものは非負整数でなければならない。
    """

    def __init__(self, n: int, default: int = 0, lst: list[int] = None, first_ver: int = 0):
        """
        n: 配列のサイズ
        default: 配列の初期値
        lst: 永続配列にしたい配列
        first_ver: 最初の version 番号
        構築は O(n) で行われる。
        """
        assert 0 < n
        assert 0 <= first_ver
        assert 0 <= default
        assert isinstance(default, int)
        self.mask30 = (1 << 30) - 1
        self.size = n
        self.k = (n - 1).bit_length()  # 木の高さ (根を高さ 0 としたときの葉の高さ)
        assert self.k <= 30
        self.size2 = 1 << self.k  # 内部的なサイズ。n 以上の最小の 2 べき。
        self.tree = [0 for _ in range(2 * self.size2 - 1)]  # 木は内部的にも 0-indexed としている
        self.default = default
        if lst is None:
            lst_ = [default] * self.size2
        else:
            assert len(lst) == self.size
            assert all(0 <= x for x in lst)
            lst_ = lst[:]
            lst_ += [default] * (self.size2 - self.size)
        for i in range(self.size2):  # 葉の値の設定
            self.tree[self.size2 + i - 1] = lst_[i] << 60
        for i in range(self.size2 - 1):  # 葉以外の子ノードの設定
            self.tree[i] = (((i << 1) + 1) << 30) + (i << 1) + 2
        self.ver_list = [-1] * first_ver + [0]

    def get(self, t: int, i: int):
        """version t における index i の値を出力。O(log n)"""
        assert 0 <= t < len(self.ver_list) and self.ver_list[t] != -1, f"No such version exists: {t}"
        assert 0 <= i < self.size2, i
        ind = self.ver_list[t]  # ver t の根
        mask = 1 << (self.k - 1)
        while mask:
            if i & mask:
                ind = self.tree[ind] & self.mask30
            else:
                ind = (self.tree[ind] >> 30) & self.mask30
            mask >>= 1
        return self.tree[ind] >> 60

    def update(self, t_old: int, t_new: int, i: int, val: int):
        """version t_old の index i を val に変更したものを version t_new とする。O(log n)"""
        assert 0 <= t_old < len(self.ver_list) and self.ver_list[t_old] != -1, f"No such version exists: {t_old}"
        assert 0 <= i < self.size2, i
        self.ver_list += [-1] * (t_new - len(self.ver_list) + 1)
        assert self.ver_list[t_new] == -1, f"version already exists: {t_new}"
        self.ver_list[t_new] = len(self.tree)
        ind_old = self.ver_list[t_old]
        mask = 1 << (self.k - 1)
        while mask:
            new_node = 0
            if i & mask:
                new_node_lch = (self.tree[ind_old] >> 30) & self.mask30
                new_node_rch = len(self.tree) + 1  # この Node は次のループ or 抜けた後で追加
                new_node = (new_node_lch << 30) | new_node_rch
                ind_old = self.tree[ind_old] & self.mask30
            else:
                new_node_lch = len(self.tree) + 1  # この Node は次のループ or 抜けた後で追加
                new_node_rch = self.tree[ind_old] & self.mask30
                new_node = (new_node_lch << 30) | new_node_rch
                ind_old = (self.tree[ind_old] >> 30) & self.mask30
            self.tree.append(new_node)
            mask >>= 1
        self.tree.append(val << 60)

    def copy(self, t_old: int, t_new: int) -> None:
        """version t_old を version t_new にコピーする。O(log n)"""
        self.update(t_old, t_new, 0, self.get(t_old, 0))

    def get_all(self, t: int) -> list[int]:
        """version t における配列を出力。O(n)"""
        assert 0 <= t < len(self.ver_list) and self.ver_list[t] != -1, f"No such version exists: {t}"
        inds = [self.ver_list[t]]
        for _ in range(self.k):
            new_inds = []
            for ind in inds:
                new_inds.append((self.tree[ind] >> 30) & self.mask30)
                new_inds.append(self.tree[ind] & self.mask30)
            inds = new_inds
        return [self.tree[ind] >> 60 for ind in inds]

    def __getitem__(self, ti: tuple[int, int]) -> int:
        """ar[t, i] で ar.get(t, i) と同じことができる。O(log n)"""
        return self.get(ti[0], ti[1])


# -----


class Node:
    """永続配列用のノード"""

    def __init__(self, val=None):
        """通常は「lch と rch」「val」のうちの一方のみを持つ"""
        self.lch = None  # 左の子ノードの index
        self.rch = None  # 右の子ノードの index
        self.val = val


class PersistentArray:
    """永続配列 (完全二分木)。O(log n) で各種操作が可能。"""

    def __init__(self, n: int, default=0, lst: list = None, first_ver: int = 0):
        """
        n: 配列のサイズ
        default: 配列の初期値
        lst: 永続配列にしたい配列
        first_ver: 最初の version 番号
        構築は O(n) で行われる。
        """
        assert 0 < n
        assert 0 <= first_ver
        self.size = n
        self.k = (n - 1).bit_length()  # 木の高さ (根を高さ 0 としたときの葉の高さ)
        self.size2 = 1 << self.k  # 内部的なサイズ。n 以上の最小の 2 べき。
        self.tree = [Node() for _ in range(2 * self.size2 - 1)]  # 木は内部的にも 0-indexed としている
        self.default = default
        if lst is None:
            lst_ = [default] * self.size2
        else:
            assert len(lst) == self.size
            lst_ = lst[:]
            lst_ += [default] * (self.size2 - self.size)
        for i in range(self.size2):  # 葉の値の設定
            self.tree[self.size2 + i - 1].val = lst_[i]
        for i in range(self.size2 - 1):  # 葉以外の子ノードの設定
            self.tree[i].lch = (i << 1) + 1
            self.tree[i].rch = (i << 1) + 2
        self.ver_list = [-1] * first_ver + [0]

    def get(self, t: int, i: int):
        """version t における index i の値を出力。O(log n)"""
        assert 0 <= t < len(self.ver_list) and self.ver_list[t] != -1, f"No such version exists: {t}"
        assert 0 <= i < self.size2, i
        ind = self.ver_list[t]  # ver t の根
        mask = 1 << (self.k - 1)
        while mask:
            if i & mask:
                ind = self.tree[ind].rch
            else:
                ind = self.tree[ind].lch
            mask >>= 1
        return self.tree[ind].val

    def update(self, t_old: int, t_new: int, i: int, val):
        """version t_old の index i を val に変更したものを version t_new とする。O(log n)"""
        assert 0 <= t_old < len(self.ver_list) and self.ver_list[t_old] != -1, f"No such version exists: {t_old}"
        assert 0 <= i < self.size2, i
        self.ver_list += [-1] * (t_new - len(self.ver_list) + 1)
        assert self.ver_list[t_new] == -1, f"version already exists: {t_new}"
        self.ver_list[t_new] = len(self.tree)
        ind_old = self.ver_list[t_old]
        mask = 1 << (self.k - 1)
        while mask:
            new_node = Node()
            if i & mask:
                new_node.lch = self.tree[ind_old].lch
                new_node.rch = len(self.tree) + 1  # この Node は次のループ or 抜けた後で追加
                ind_old = self.tree[ind_old].rch
            else:
                new_node.lch = len(self.tree) + 1  # この Node は次のループ or 抜けた後で追加
                new_node.rch = self.tree[ind_old].rch
                ind_old = self.tree[ind_old].lch
            self.tree.append(new_node)
            mask >>= 1
        self.tree.append(Node(val))

    def copy(self, t_old: int, t_new: int) -> None:
        """version t_old を version t_new にコピーする。O(log n)"""
        self.update(t_old, t_new, 0, self.get(t_old, 0))

    def get_all(self, t: int) -> list:
        """version t における配列を出力。O(n)"""
        assert 0 <= t < len(self.ver_list) and self.ver_list[t] != -1, f"No such version exists: {t}"
        inds = [self.ver_list[t]]
        for _ in range(self.k):
            new_inds = []
            for ind in inds:
                new_inds.append(self.tree[ind].lch)
                new_inds.append(self.tree[ind].rch)
            inds = new_inds
        return [self.tree[ind].val for ind in inds]

    def __getitem__(self, ti: tuple[int, int]):
        """ar[t, i] で ar.get(t, i) と同じことができる。O(log n)"""
        return self.get(ti[0], ti[1])
