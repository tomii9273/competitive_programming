# ブロックサイズ b ごとに階乗 mod 素数を計算したリストを作成する。
# 正確には、n = 1, 2, ..., (bn が p を超えないような最大の n) について順に (bn)! mod p を計算・追加し、最終要素に (p - 1)! ≡ p - 1 を追加したもの。
# https://judge.yosupo.jp/problem/many_factorials などの埋め込み解法に使える。
# 実行時間は数分。

# p は素数
# p = 998244353
p = 10**9 + 7
le = p

# リストの長さ (の目安)。AtCoder の提出上限の 512 kiB、(1 文字 1 バイトである) 数値とカンマの文字数を 11 として計算。
# 実際には (最大) 9 桁 + カンマ 1 文字で 10 文字なので、提出コードにリストを貼り付けるだけで上限に達することはなく、その下に書く余裕ができる。
n = (512 * 1024) // 11
print(f"{n=}")

# ブロックサイズ (いくつごとに階乗をリストに保存するか)。実用的には、数万以下が望ましい (それくらいになる)。
b = le // n
print(f"{b=}")

mul_list = [1]
mul = 1
for i in range(1, le):
    mul = (mul * i) % p
    if i % b == 0:
        mul_list.append(mul)
    if i % 10**7 == 0:
        print(f"{i=}, {mul=}")
mul_list.append(mul)

with open(f"mul_list_mod_{p}_bs_{b}_len_{len(mul_list)}.txt", "w") as f:
    f.write(str(mul_list).replace(" ", ""))
