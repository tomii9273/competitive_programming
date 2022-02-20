n = int(input())
C = [list(map(int, input().split())) for i in range(n - 1)]  # 木でない場合は変える

for i in range(len(C)):  # 入力が 1-indexed の場合
    for j in range(2):
        C[i][j] -= 1


M = [[] for i in range(n)]
for i in range(len(C)):
    M[C[i][0]].append(C[i][1])
    M[C[i][1]].append(C[i][0])  # 有向グラフの場合は削除！！


s = 0  # 始点の番号

P = [-1] * n  # iの親ノードの番号（最短路などの復元用）
D = [-1] * n  # 始点からiまでの最短距離（兼訪問フラグ）

Q = [(s, 0)]  # キュー（見た順）
ind = 0
D[s] = 0
while ind < len(Q):
    i, d = Q[ind]
    for x in M[i]:
        if D[x] == -1:
            D[x] = d + 1
            P[x] = i
            Q.append((x, d + 1))
    ind += 1


# ----- グラフが木の場合で、そこ以深のノード総数を数える場合（自分自身も含める） -----


n = int(input())
C = [list(map(int, input().split())) for i in range(n - 1)]  # 木でない場合は変える

for i in range(len(C)):  # 入力が 1-indexed の場合
    for j in range(2):
        C[i][j] -= 1


M = [[] for i in range(n)]
for i in range(len(C)):
    M[C[i][0]].append(C[i][1])
    M[C[i][1]].append(C[i][0])  # 有向グラフの場合は削除！！


s = 0  # 始点の番号

P = [-1] * n  # iの親ノードの番号（最短路などの復元用）
D = [-1] * n  # 始点からiまでの最短距離
TQ = []  # 末端のノードの番号を保存する

Q = [(s, 0)]
ind = 0
D[s] = 0
while ind < len(Q):
    is_tail = True  # 末端かどうかのフラグ
    i, d = Q[ind]
    for x in M[i]:
        if D[x] == -1:
            is_tail = False
            D[x] = d + 1
            P[x] = i
            Q.append((x, d + 1))
    if is_tail:
        TQ.append(i)
    ind += 1

DN = [1] * n  # i以深のノード総数（i自身も含める）
CN = [0] * n  # iの子ノードのうちいくつを数え終えたかを管理する
ind = 0

while ind < len(TQ):
    i = TQ[ind]
    if P[i] != -1:
        p = P[i]
        CN[p] += 1
        DN[p] += DN[i]
        if p != s and CN[p] == len(M[p]) - 1:  # pの子ノードをすべて数え終えた
            TQ.append(p)
    ind += 1
