#ifdef TEST // 「g++ -DTEST tp.cpp」のようにコンパイルすると下の行が実行される
#define _GLIBCXX_DEBUG
#endif
#include <bits/stdc++.h>
using namespace std;
using ll = int64_t;
#define rep(i, n) for (ll i = 0; i < (ll)(n); i++)
#define rep2(i, s, n) for (ll i = (s); i < (ll)(n); i++)
#define all(v) v.begin(), v.end()

int main()
{
  // O((V + E)log(V))
  // Cは [[スタート頂点, ゴール頂点, 重み], ...] のリスト

  vector<vector<vector<ll>>> M(n);
  for (ll i = 0; i < C.size(); i++)
  {
    M[C[i][0]].push_back({C[i][1], C[i][2]}); // 無向グラフなら両方追加
    M[C[i][1]].push_back({C[i][0], C[i][2]}); // 無向グラフなら両方追加
  }

  ll s = 0;            // スタート地点のindex
  ll big = pow(10, 9); // 距離infを示す巨大な数

  vector<ll> D(n, big); // 頂点sからの距離
  vector<ll> P(n, -1);  // 頂点sからの最短距離において、そこの直前の頂点(経路復元に利用)
  D[s] = 0;
  vector<ll> V(n, 0);             // その頂点のD[i]が最短距離と確定したら1
  priority_queue<pair<ll, ll>> Q; // 優先度付きキュー
  ll le, u, du, luv, alt, v;
  pair<ll, ll> q;

  Q.push(make_pair(0, s));

  while (Q.size() > 0)
  {
    q = Q.top();
    Q.pop();
    u = q.second;
    du = -q.first;
    if (V[u] == 0)
    {
      V[u] = 1;
      for (ll i = 0; i < M[u].size(); i++)
      {
        v = M[u][i][0];
        luv = M[u][i][1];
        if (V[v] == 0)
        {
          alt = du + luv;
          if (D[v] > alt)
          {
            D[v] = alt;
            P[v] = u;
            Q.push(make_pair(-alt, v));
          }
        }
      }
    }
  }
}
