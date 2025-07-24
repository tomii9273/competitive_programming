import sys

sys.path.append("../")
from library.binary_trie import BinaryTrie, BinaryTrieBit


def test_binary_trie():

    def test_one(trie):
        # 初期状態
        assert trie.count(0) == 0
        assert trie.get_min_xor(0) == -1

        # add のテスト
        trie.add(5, 3)
        assert trie.count(5) == 3
        trie.add(5)
        assert trie.count(5) == 4
        trie.add(10, 2)
        assert trie.count(10) == 2

        # one のテスト
        assert trie.one(7) == 1  # 新規追加される
        assert trie.count(7) == 1
        assert trie.one(7) == 1  # すでにあるので追加されない

        # remove のテスト
        assert trie.remove(5, 2) == 2
        assert trie.count(5) == 2
        assert trie.remove(5, 10) == 2  # 残り全て削除される
        assert trie.count(5) == 0
        assert trie.remove(5) == 0  # すでに削除済み

        # get_min_xor のテスト
        # trie には 10, 7 が残っている
        # x = 0: 最小 xor は 7 ^ 0 = 7, 10 ^ 0 = 10 → 7
        assert trie.get_min_xor(0) == 7
        # x = 7: 最小 xor は 7 ^ 7 = 0, 10 ^ 7 = 13 → 7
        assert trie.get_min_xor(7) == 7
        # x = 9: 最小 xor は 7 ^ 9 = 14, 10 ^ 9 = 3 → 10
        assert trie.get_min_xor(9) == 10

        trie.add(1000000)
        # trie には 1000000, 10, 7 が残っている
        assert trie.count(1000000) == 1
        assert (
            trie.get_min_xor(524288) == 1000000
        )  # 最小 xor は 7 ^ 524288  = 524295、10 ^ 524288 = 524298、1000000 ^ 524288 = 475712 (524288 = 2 ** 19)

    test_one(BinaryTrie(20))
    print("BinaryTrie: All tests passed.")
    test_one(BinaryTrieBit(20))
    print("BinaryTrieBit: All tests passed.")


if __name__ == "__main__":
    test_binary_trie()
