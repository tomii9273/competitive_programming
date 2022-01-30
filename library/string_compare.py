alp = [[chr(i) for i in range(ord("a"), ord("z") + 1)],
       [chr(i) for i in range(ord("A"), ord("Z") + 1)],
       [str(i) for i in range(10)]]
alpd = [{}, {}, {}]

for i in range(3):
    for j in range(len(alp[i])):
        alpd[i][alp[i][j]] = j

# 文字列/リストであるsとtを辞書順で比較する。sが早いなら0を、sとtが同一なら1を、sが遅いなら2を、空の文字列/リストがあるなら3を返す。
# 英小文字、英大文字、数字に対応。数字はint型でも可。
# pythonでは文字列やリストのsortができるので、あまり出番はないかも。


def dc(s, t):
    if isinstance(s, int):
        s = str(s)
        t = str(t)

    ls = len(s)
    lt = len(t)
    if ls == 0 or lt == 0:
        return 3

    typ = 0
    if s[0] in alp[1]:
        typ = 1
    if s[0] in alp[2]:
        typ = 2

    for i in range(min(ls, lt)):
        if alpd[typ][s[i]] < alpd[typ][t[i]]:
            return 0
        elif alpd[typ][s[i]] > alpd[typ][t[i]]:
            return 2
    if ls < lt:
        return 0
    if ls > lt:
        return 2
    return 1


print(dc(0, 0))
