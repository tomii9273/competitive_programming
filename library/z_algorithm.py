# 参考: https://qiita.com/t_fuki/items/e682238dda6ad832ce05


def z_algorithm(s: str) -> list[int]:
    """s と s[i:] の最長共通接頭辞 (LCP) の長さの配列を求める。O(len(s))"""
    z = [0] * len(s)
    z[0] = len(s)
    ind_l = 0  # Z[ind_l] の結果を i で再利用できるかもしれない
    ind_r = 0  # s[ind_r - 1] まで調べてある
    for i in range(1, len(s)):
        if z[i - ind_l] < ind_r - i:  # 過去の結果をそのまま使える
            z[i] = z[i - ind_l]
        else:  # 過去の結果をそのまま使えない。s[ind_r] 以降を一つずつ調べる
            ind_r = max(ind_r, i)
            while ind_r < len(s) and s[ind_r] == s[ind_r - i]:
                ind_r += 1
            z[i] = ind_r - i
            ind_l = i
    return z
