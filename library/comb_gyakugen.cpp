#ifdef TEST // 「g++ -DTEST tp.cpp」のようにコンパイルすると下の行が実行される
#define _GLIBCXX_DEBUG
#endif
#include <bits/stdc++.h>
using namespace std;
using ll = int64_t;
#define rep(i, n) for (ll i = 0; i < (ll)(n); i++)
#define rep2(i, s, n) for (ll i = (s); i < (ll)(n); i++)
#define all(v) v.begin(), v.end()

ll pow(ll x, ll y, ll mod)
{
  x %= mod;
  ll ans = 1;
  while (y > 0)
  {
    if (y % 2 == 1)
    {
      ans = (ans * x) % mod;
    }
    x = (x * x) % mod;
    y /= 2;
  }
  return ans % mod;
}

ll inv(ll x, ll mod)
{
  x %= mod;
  if (x == 2)
  {
    return (mod + 1) / 2;
  }
  return pow(x, mod - 2, mod);
}

struct Combi
{
  int le, mod;
  vector<ll> M;  // i!
  vector<ll> MI; // i!の逆元

  Combi(int le_, int mod_)
  {
    le = le_;
    mod = mod_;
    ll mul = 1;
    M.push_back(1); // i!
    rep2(i, 1, le)
    {
      mul = (mul * i) % mod;
      M.push_back(mul);
    }

    rep(i, le) { MI.push_back(0); } // i!の逆元
    MI[le - 1] = inv(M[le - 1], mod);
    for (int i = le - 2; i >= 0; i--)
    {
      MI[i] = (MI[i + 1] * (i + 1)) % mod;
    }
  }

  ll C(ll x, ll y) // コンビネーション (組合せ, 二項係数)
  {
    if (y < 0 || y > x)
    {
      return 0;
    }
    else if (x >= le) // O(min(y, x-y))
    {
      y = min(y, x - y);
      ll ans = 1;
      for (int i = x; i > x - y; i--)
      {
        ans = (ans * i) % mod;
      }
      return (ans * MI[y]) % mod;
    }
    else // O(1)
    {
      ll ans = M[x];
      ans = (ans * MI[y]) % mod;
      return (ans * MI[x - y]) % mod;
    }
  }

  ll H(ll x, ll y) // 重複組合せ、x + y < le にすることに注意
  {
    return C(x + y - 1, y);
  }

  ll P(ll x, ll y) // パーミュテーション (順列)
  {
    if (y < 0 || y > x)
    {
      return 0;
    }
    else if (x > le) // O(min(y, x-y))
    {
      y = min(y, x - y);
      ll ans = 1;
      for (int i = x; i > x - y; i--)
      {
        ans = (ans * i) % mod;
      }
      return ans % mod;
    }
    else // O(1)
    {
      ll ans = M[x];
      return (ans * MI[x - y]) % mod;
    }
  }
};