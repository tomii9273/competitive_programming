#ifdef TEST // 「g++ -DTEST tp.cpp」のようにコンパイルすると下の行が実行される
#define _GLIBCXX_DEBUG
#endif
#include <bits/stdc++.h>
using namespace std;
using ll = int64_t;
#define rep(i, n) for (ll i = 0; i < (ll)(n); i++)
#define rep2(i, s, n) for (ll i = (s); i < (ll)(n); i++)
#define all(v) v.begin(), v.end()

// a,bの積を計算し、二進数表記の(61桁目以上, 1-60桁目)を十進数で返す。
// 制約：a,bは非負整数で2^60未満。(10^18 < 2^60)
pair<ll, ll> mul(ll a, ll b)
{
  ll a0, a1, b0, b1, c0, c1, c2, ans0, ans1;
  a0 = a & ((1 << 30) - 1);
  a1 = a >> 30;
  b0 = b & ((1 << 30) - 1);
  b1 = b >> 30;

  c0 = a0 * b0;
  c1 = a0 * b1 + b0 * a1;
  c2 = a1 * b1;

  ans0 = c0 + ((c1 & ((1 << 30) - 1)) << 30);
  ans1 = c2 + (c1 >> 30);
  return make_pair(ans1, ans0);
}

int main()
{
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
}
