def sa_is(s_num: list) -> list:
    """
    SA-IS法。
    整数からなるリストs_numを入力すると、s_numの接尾辞配列を出力する。
    n = len(s_num), m = max(s_num) とすると、時間計算量:O(n * m)
    """
    n = len(s_num)  # リスト長

    # 最小値が1となるようにシフト
    shift = -min(s_num) + 1
    for i in range(n):
        s_num[i] += shift

    s_num.append(0)  # 終端文字0を追加
    n += 1
    m = max(s_num) + 1  # 整数の種類数

    count_s = [0] * m  # 各数字の個数のリスト
    for item in s_num:
        count_s[item] += 1

    type_list = [0] * n  # 接尾辞のtypeのリスト。0:L-type, 1:S-type, 2:LMS-type
    type_list[n - 1] = 1  # 終端文字はS-typeとする
    LMS_list = []  # LMS-typeである接尾辞のindexのリスト

    # typeを計算
    for i in range(n - 2, -1, -1):
        if s_num[i] < s_num[i + 1]:
            type_list[i] = 1
        elif s_num[i] == s_num[i + 1]:
            type_list[i] = type_list[i + 1]
    for i in range(1, n):
        if type_list[i - 1] == 0 and type_list[i] == 1:
            type_list[i] = 2
            LMS_list.append(i)

    ### induced sorting 1回目（ここでは正しい接尾辞配列はまだ得られない。LMS-type接尾辞を、ほぼ辞書順に並べるためだけのもの。） ###

    # LMS-substring(「LMS-type接尾辞の先頭文字～直後のLMS-type接尾辞の先頭文字」を切り取ったもの)の中に重複するものがない場合は、このsortingで
    # LMS-type接尾辞は完全に辞書順に並ぶ。重複がある場合は、それを含むLMS-type接尾辞は完全には辞書順に並ばないので、後述する再帰が必要となる。

    bac = [-1] * n  # induced sortingのための先頭文字バケットを作成
    bac_start = [0]  # バケット中の各先頭文字の開始位置を示すリスト（count_sの累積和をとったもの）
    for i in range(m):
        bac_start.append(count_s[i] + bac_start[-1])

    # LMS-typeを格納（1回目なので、順番はてきとう）
    bac_start_1 = bac_start[:]
    for i in LMS_list:
        ini = s_num[i]
        bac[bac_start_1[ini + 1] - 1] = i
        bac_start_1[ini + 1] -= 1

    # 配列を前方から走査し、入っているLMS-typeを元に、L-typeを格納（LMS-typeは一旦削除）
    bac_start_1 = bac_start[:]
    for i in range(n):
        j = bac[i]
        if j != -1:
            if type_list[j - 1] == 0:
                bac[bac_start_1[s_num[j - 1]]] = j - 1
                bac_start_1[s_num[j - 1]] += 1
                if j != n - 1 and type_list[j] == 2:
                    bac[i] = -1

    # 配列を後方から走査し、入っているL-typeを元に、S-type(LMS-typeも)を格納
    bac_start_1 = bac_start[:]
    steps = bac.count(-1)  # 残ステップ数。これが0になったらsortが終了しているので、ループをbreakする。
    for i in range(n - 1, 0, -1):
        j = bac[i]
        if j != -1:
            if j - 1 != -1 and type_list[j - 1] >= 1:
                bac[bac_start_1[s_num[j - 1] + 1] - 1] = j - 1
                bac_start_1[s_num[j - 1] + 1] -= 1
                steps -= 1
        if steps == 0:
            break

    ### LMS-substringに重複があるかどうか確認 ###

    name = 0  # LMS-substringにつける名前としての数字（重複する接尾辞には同じ名前がつく）
    prev_item = -1  # 下記のループ内で、前回閲覧したLMS-substringのindexを示す（LMS-substringは辞書順に並んでいるので、隣接するもの同士の比較だけで十分）
    LMS_num = {}  # LMS-substringのindexと名前を保存する辞書

    # 辞書の作成
    for item in bac:
        if type_list[item] == 2:
            for i in range(n):
                if prev_item == -1 or s_num[item + i] != s_num[prev_item + i]:
                    name += 1
                    prev_item = item
                    break
                elif i > 0 and (type_list[item + i] == 2 or type_list[prev_item + i] == 2):
                    break
            LMS_num[item] = name

    if name < len(LMS_list):  # 重複がある場合
        sub_list = []  # LMS-substringの名前を、元々の（関数に与えたリストに含まれていたときの）順番で入れるためのリスト
        for item in LMS_list:
            sub_list.append(LMS_num[item])

        sub_list_SAISed = sa_is(sub_list)  # 「LMS-substringの名前の列のリスト」を再帰的に関数に入力しているが、これにより、LMS-type接尾辞の辞書順における並び方を求めている

        LMS_list = [LMS_list[item] for item in sub_list_SAISed]  # 上の行の結果をもとに、LMS-type接尾辞を辞書順に並べる

    else:  # 重複がない場合
        # バケットからそのままの順番でLMS-type接尾辞だけ取り出せばよい（辞書順になっている）
        LMS_list = []
        for item in bac:
            if type_list[item] == 2:
                LMS_list.append(item)

    LMS_list = [LMS_list[len(LMS_list) - 1 - i] for i in range(len(LMS_list))]  # induced sortingのために逆順にしておく

    ### induced sorting 2回目（今回はLMS-type接尾辞を正しい順番で格納する。今回のsort後に得られる配列が、接尾辞配列となる。） ###

    bac = [-1] * n  # induced sortingのための先頭文字バケットを作成

    # LMS-typeを格納（2回目なので、正しい順番で入れられる）
    bac_start_1 = bac_start[:]
    for i in LMS_list:
        ini = s_num[i]
        bac[bac_start_1[ini + 1] - 1] = i
        bac_start_1[ini + 1] -= 1

    # 配列を前方から走査し、入っているLMS-typeを元に、L-typeを格納（LMS-typeは一旦削除）
    bac_start_1 = bac_start[:]
    for i in range(n):
        j = bac[i]
        if j != -1:
            if type_list[j - 1] == 0:
                bac[bac_start_1[s_num[j - 1]]] = j - 1
                bac_start_1[s_num[j - 1]] += 1
                if j != n - 1 and type_list[j] == 2:
                    bac[i] = -1

    # 配列を後方から走査し、入っているL-typeを元に、S-type(LMS-typeも)を格納
    bac_start_1 = bac_start[:]
    steps = bac.count(-1)  # 残ステップ数。これが0になったらsortが終了しているので、ループをbreakする。
    for i in range(n - 1, 0, -1):
        j = bac[i]
        if j != -1:
            if j - 1 != -1 and type_list[j - 1] >= 1:
                bac[bac_start_1[s_num[j - 1] + 1] - 1] = j - 1
                bac_start_1[s_num[j - 1] + 1] -= 1
                steps -= 1
        if steps == 0:
            break

    bac = bac[1:]  # 接尾辞配列の先頭は終端文字なので削除

    return bac


def make_suffix_array(s_num: list) -> list:
    """
    Manber & Myers のアルゴリズム。
    整数からなるリストs_numを入力すると、s_numの接尾辞配列を出力する。
    n = len(s_num) とすると、時間計算量:O(n * (log n)^2)
    参考:『プログラミングコンテストチャレンジブック 第2版』(蟻本) P.336-337
    """
    n = len(s_num)

    # 最小値が0となるようにシフト
    shift = -min(s_num)
    for i in range(n):
        s_num[i] += shift

    ANS = [-1] * n

    L = [[-1, -1, i] for i in range(n)]
    for i in range(n):
        L[i][1] = s_num[i]
    L.sort()
    ind = 0
    for i in range(n):
        if i > 0 and L[i][:2] != L[i - 1][:2]:
            ind += 1
        ANS[L[i][2]] = ind

    shift = 1
    while shift < n:
        for i in range(n):
            L[i][0] = L[i][1]
        for i in range(n):
            L[i][1] = ANS[L[i][2] + shift] if L[i][2] + shift < n else -1
        L.sort()

        ind = 0
        for i in range(n):
            if i > 0 and L[i][:2] != L[i - 1][:2]:
                ind += 1
            ANS[L[i][2]] = ind
        for i in range(n):
            L[i][1] = ANS[L[i][2]]

        shift *= 2

    return [L[i][2] for i in range(n)]
