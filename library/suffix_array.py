def sa_is(s_num_: list[int]) -> list[int]:
    """
    SA-IS 法。
    整数からなるリスト s_num_ を入力すると、s_num_ の接尾辞配列を出力する。
    n = len(s_num_), m = max(s_num_) とすると、時間計算量:O(n * m)
    """
    s_num = s_num_[:]
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

    # ### induced sorting 1回目（ここでは正しい接尾辞配列はまだ得られない。LMS-type接尾辞を、ほぼ辞書順に並べるためだけのもの。） ###

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

    # ### LMS-substringに重複があるかどうか確認 ###

    name = 0  # LMS-substringにつける名前としての数字（重複する接尾辞には同じ名前がつく）

    # 下記のループ内で、前回閲覧したLMS-substringのindexを示す（LMS-substringは辞書順に並んでいるので、隣接するもの同士の比較だけで十分）
    prev_item = -1
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
        # LMS-substringの名前を、元々の（関数に与えたリストに含まれていたときの）順番で入れるためのリスト
        sub_list = []
        for item in LMS_list:
            sub_list.append(LMS_num[item])

        # 「LMS-substringの名前の列のリスト」を再帰的に関数に入力しているが、これにより、LMS-type接尾辞の辞書順における並び方を求めている
        sub_list_SAISed = sa_is(sub_list)

        LMS_list = [LMS_list[item] for item in sub_list_SAISed]  # 上の行の結果をもとに、LMS-type接尾辞を辞書順に並べる

    else:  # 重複がない場合
        # バケットからそのままの順番でLMS-type接尾辞だけ取り出せばよい（辞書順になっている）
        LMS_list = []
        for item in bac:
            if type_list[item] == 2:
                LMS_list.append(item)

    LMS_list = [LMS_list[len(LMS_list) - 1 - i] for i in range(len(LMS_list))]  # induced sortingのために逆順にしておく

    # ### induced sorting 2回目（今回はLMS-type接尾辞を正しい順番で格納する。今回のsort後に得られる配列が、接尾辞配列となる。）

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


def make_suffix_array(s_num: list[int]) -> list[int]:
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


def make_lcp_array(array: list[int], suffix_array: list[int]) -> list[int]:
    """
    Kasai のアルゴリズムで、元々の配列と接尾辞配列から LCP 配列
    (一つ前の接尾辞との最長共通接頭辞の長さの配列) を構築。O(len(array))
    """

    assert len(array) == len(suffix_array)

    n = len(suffix_array)
    index_list = [0] * n
    for i in range(n):
        index_list[suffix_array[i]] = i  # 接尾辞配列の各値があるindexを保存するリスト

    lcp_array = [-1] * n
    lcp_array[0] = 0
    h = 0

    for i in range(n):
        ind_i = index_list[i]
        if ind_i == 0:
            continue
        j = suffix_array[ind_i - 1]
        while i + h <= n - 1 and j + h <= n - 1 and array[i + h] == array[j + h]:
            h += 1
        lcp_array[ind_i] = h
        h = max(0, h - 1)

    return lcp_array


from min_queue import MinQueue


def longest_common_substring(str_list: list[str]) -> tuple[int, list[int]]:
    """
    str_list 内の全ての文字列に共通して現れる最長の部分文字列を 1 つ探し、その長さ・各文字列での開始位置 (存在しない場合は -1) を返す。
    文字列が 1 つの場合は、その文字列に (異なる開始位置で) 複数回現れる最長の部分文字列を 1 つ探し、
    その長さ・開始位置 2 か所 (存在しない場合は -1) を返す。
    """
    n_str = len(str_list)
    s = []
    index_to_strno = []  # 何文字目が何番目の文字列由来か

    # 文字列を数値に変換して繋げる
    for i in range(n_str):
        s += [ord(c) - ord("A") for c in str_list[i]]
        s += [100 + i]  # 終端文字、区切り文字
        index_to_strno += [i] * (len(str_list[i]) + 1)

    suffix_array = sa_is(s)
    lcp_array = make_lcp_array(s, suffix_array)

    # 文字列が 1 つの場合
    if n_str == 1:
        max_length = max(lcp_array)
        if max_length == 0:
            return 0, [-1, -1]
        else:
            ind = lcp_array.index(max_length)
            return max_length, sorted([suffix_array[ind], suffix_array[ind - 1]])

    max_length = 0  # 共通して現れる最長の部分文字列の長さ
    ans = [-1] * n_str  # 各文字列での最長の部分文字列の開始位置

    distinct = 0  # 枠内の文字列の種類数
    now = [0] * n_str  # 枠内の各種類の文字列の個数
    rightest = [-1] * n_str  # 枠内の各種類の文字列のうち一番右 (後) のものの index
    ind_left = 0  # 枠の左端

    minq = MinQueue()  # LCP 配列管理用
    pop_cnt = 0  # minq から pop する回数の管理用

    for i in range(len(s)):
        # 種類数が足りない場合、枠を右に広げる
        if distinct < n_str:
            tmp_ind = index_to_strno[suffix_array[i]]
            now[tmp_ind] += 1
            if now[tmp_ind] == 1:
                distinct += 1
            rightest[tmp_ind] = suffix_array[i]
            minq.push(lcp_array[i])

        # 種類数が十分な場合、枠の左を可能な限り狭めてから max_length 候補を取得
        if distinct == n_str:
            while True:
                tmp_ind = index_to_strno[suffix_array[ind_left]]
                if now[tmp_ind] == 1:
                    break
                now[tmp_ind] -= 1
                pop_cnt += 1
                ind_left += 1

            # LCP 配列は「1 つ前」との比較なので、lcp_array[枠の左端] は考慮すべきでない。そのため 1 つ多く削除する。
            while pop_cnt > -1:
                minq.pop()
                pop_cnt -= 1

            if minq.get_min() > max_length:
                max_length = minq.get_min()
                shift = 0
                ans = []
                for i in range(n_str):
                    ans.append(rightest[i] - shift)
                    shift += len(str_list[i]) + 1

            # 枠の左をもう一つ狭めて、種類数が十分な状態から足りない状態へ移行
            tmp_ind = index_to_strno[suffix_array[ind_left]]
            now[tmp_ind] -= 1
            distinct -= 1
            pop_cnt += 1
            ind_left += 1

    return max_length, ans
