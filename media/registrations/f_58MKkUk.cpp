#include <bits/stdc++.h>
using namespace std;
typedef long long int ll;
#define pb push_back
#define mp make_pair
std::vector<int> adj[200005];
int depth[200005] = {0}, par[200005] = {0}, subsize[200005] = {0}, chainTop[200005], otherEnd[200005];
std::vector<int> chains[200005];
int dfs(int cur, int prev, int dep) {
    par[cur] = prev;
    depth[cur] = dep;
    int sz = adj[cur].size();
    subsize[cur] = 1;
    for(int i = 0; i < sz; i++) {
        if(adj[cur][i] != prev) {
            subsize[cur] += dfs(adj[cur][i], cur, dep + 1);
        }
    }
    return subsize[cur];
}
void hld(int cur, int prev, int top) {
    chainTop[cur] = top;
    chains[top].pb(cur);
    int sz = adj[cur].size();
    int mx = 0;
    int idx = -1;
    for(int i = 0; i < sz; i++) {
        if(adj[cur][i] != prev) {
            if(subsize[adj[cur][i]] > mx) {
                mx = subsize[adj[cur][i]];
                idx = i;
            }
        }
    }

    for(int i = 0; i < sz; i++) {
        if(adj[cur][i] != prev) {
            if(idx == i) {
                hld(adj[cur][i], cur, top);
            }
            else {
                hld(adj[cur][i], cur, adj[cur][i]);
            }
        }
    }
    if(sz == 1) {
        otherEnd[top] = cur;
    }
    return;
}
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    int n, i, j, k;
    cin >> n;
    for(i = 0; i < n - 1; i++) {
        cin >> j >> k;
        adj[j].pb(k);
        adj[k].pb(j);
    }
    dfs(1, 1, 0);
    hld(1, 1, 1);
    cout << "d " << 1 << endl;
    cout.flush();
    int depx;
    cin >> depx;
    int u = 1, v = otherEnd[1];
    while(1) {
        int dist;
        cout << "d " << v << endl;
        cout.flush();
        cin >> dist;
        int depy = (depx + depth[v] - dist) / 2;
        if(depx == depy) {
            cout << "! " << chains[u][depy - depth[u]] << endl;
            return 0;
        }
        else {
            cout << "s " <<  chains[u][depy - depth[u]] << endl;
            cout.flush();
            cin >> u;
            v = otherEnd[u];
            if(depth[u] == depx) {
                cout << "! " << u << endl;
                return 0;
            }
        }
    }
    return 0;
}