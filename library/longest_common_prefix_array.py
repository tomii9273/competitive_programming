# SA-IS 法など、接尾辞配列を構築するアルゴリズムをここに貼る

# sa = SAIS(S)  # 接尾辞配列を構築


def lcp(S: list, sa: list) -> list:
    """
    LCP 配列 (Suffix Array (接尾辞配列) 上の隣接する suffix の LCP (最長共通接頭辞) の長さの配列) を、
    Kasai アルゴリズムで作成する。
    S: 接尾辞配列の構築に使用した、整数からなるリスト
    sa: 接尾辞配列 (0-indexed)
    参考: https://qiita.com/kgoto/items/9e28e37b8a4b15ea7230
    """

    n = len(sa)

    IND = [-1] * n
    for i in range(n):
        IND[sa[i]] = i

    ind = 0
    ANS = [0] * n

    for i in range(n):
        ind = max(ind, i)
        j = IND[i]
        if j != 0:
            k = j - 1
            while ind < n and ind + sa[k] - i < n:
                # print(ind)
                if S[ind] == S[ind + sa[k] - i]:
                    ind += 1
                else:
                    break
            ANS[j] = ind - i

    return ANS


# S の相異なる (連続する) 部分文字列の個数
# 参考: https://betrue12.hateblo.jp/entry/2020/09/09/131810
# ans = (len(sa) * (len(sa) + 1)) // 2 - sum(lcp(S, sa))
