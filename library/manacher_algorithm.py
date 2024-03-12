# 参考: https://snuke.hatenablog.com/entry/2014/12/02/235837
# 参考: https://tjkendev.github.io/procon-library/python/string/manacher.html


def manacher_algorithm(s: str, interval: bool = True) -> list[int]:
    """
    各文字・文字の間を中心とする最長の回文の半径 ((全長 + 1) / 2) の配列を求める。O(len(s))
    interval: 文字の間も中心とするか (配列長は 2 * len(s) - 1 になる)
    """
    if interval:
        # ダミー文字を挟む
        S = ["$"] * (2 * len(s) - 1)
        assert "$" not in s
        for i in range(len(s)):
            S[2 * i] = s[i]
    else:
        S = list(s)

    R = [0] * len(S)
    i = 0
    j = 0  # S[i + j - 1] まで調べてある
    while i < len(S):
        while i - j >= 0 and i + j < len(S) and S[i - j] == S[i + j]:  # 一つずつ調べる
            j += 1
        R[i] = j
        k = 1  # R[i - k] の結果を R[i + k] で再利用できるかもしれない
        while i - k >= 0 and k + R[i - k] < j:  # 過去の結果をそのまま使えるなら使う
            R[i + k] = R[i - k]
            k += 1
        i += k
        j -= k

    if interval:
        # ダミー文字の影響を除外
        for i in range(len(R)):
            if i % 2 == 0:
                R[i] = (R[i] + 1) // 2
            else:
                R[i] = R[i] // 2

        # 代わりに以下のようにすれば、R は半径ではなく全長の配列になる
        # for i in range(len(R)):
        #     if i % 2 == R[i] % 2:
        #         R[i] -= 1

    return R


# 半径 -> 全長

# R = manacher_algorithm(s)
# ans = []
# for i in range(len(R)):
#     if i % 2 == 0:
#         ans.append(R[i] * 2 - 1)
#     else:
#         ans.append(R[i] * 2)

# print(*ans)
