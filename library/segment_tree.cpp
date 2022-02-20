#ifdef TEST // 「g++ -DTEST tp.cpp」のようにコンパイルすると下の行が実行される
#define _GLIBCXX_DEBUG
#endif
#include <bits/stdc++.h>
using namespace std;
using ll = int64_t;
#define rep(i, n) for (ll i = 0; i < (ll)(n); i++)
#define rep2(i, s, n) for (ll i = (s); i < (ll)(n); i++)
#define all(v) v.begin(), v.end()

// セグメント木(最大値専用)。
struct SegtreeMax
{
  // n は最初に定めたサイズ、size2 は2の累乗の値をとるサイズ (>=n) 、f は初期値 (単位元)
  int n, f;
  int size2;
  vector<ll> tree;

  SegtreeMax(int n_, int f_ = -1001001001)
  {
    n = n_;
    f = f_;
    int i = 1;
    while (i < n)
    {
      i *= 2;
    }
    tree = vector<ll>(2 * i - 1, f);
    size2 = i;
  }

  void update(int i, ll x) // i番目の値をxに更新 (xは更新前の値より大きくなければならないわけではなさそう？)
  {
    int j = size2 + i - 1;
    tree[j] = x;
    while (j > 0)
    {
      j = (j - 1) / 2;
      tree[j] = max(tree[2 * j + 1], tree[2 * j + 2]);
    }
  }

  ll get(int a, int b, int k = 0, int le = 0, int ri = -1) // 区間[a, b)の最大値を返す
  {
    if (ri == -1)
    {
      ri = size2;
    }
    if (ri <= a || b <= le)
    {
      return f;
    }
    if (a <= le && ri <= b)
    {
      return tree[k];
    }
    ll vl = get(a, b, 2 * k + 1, le, (le + ri) / 2);
    ll vr = get(a, b, 2 * k + 2, (le + ri) / 2, ri);
    return max(vl, vr);
  }
};

// 2次元セグメント木(最大値専用)。
struct Segtree2DMax
{
  int h, w, f, size2;
  vector<SegtreeMax> tree;

  Segtree2DMax(int h_, int w_, int f_ = -1001001001)
  {
    h = h_;
    w = w_;
    f = f_;
    int i = 1;
    while (i < h)
    {
      i *= 2;
    }
    tree = vector<SegtreeMax>(2 * i - 1, SegtreeMax(w, f));
    size2 = i;
  }

  void update(int i0, int i1, ll x)
  {
    int j = size2 + i0 - 1;
    tree[j].update(i1, x);
    while (j > 0)
    {
      j = (j - 1) / 2;
      tree[j].update(i1, max(tree[2 * j + 1].get(i1, i1 + 1), tree[2 * j + 2].get(i1, i1 + 1)));
    }
  }

  ll get(int a, int b, int c, int d, int k = 0, int le = 0, int ri = -1)
  // [a, b) 行内の区間 [c, d) の最大値を返す
  {
    if (ri == -1)
    {
      ri = size2;
    }
    if (ri <= a || b <= le)
    {
      return f;
    }
    if (a <= le && ri <= b)
    {
      return tree[k].get(c, d);
    }
    ll vl = get(a, b, c, d, 2 * k + 1, le, (le + ri) / 2);
    ll vr = get(a, b, c, d, 2 * k + 2, (le + ri) / 2, ri);
    return max(vl, vr);
  }
};
