import pulp
import pickle
import networkx as nx

def solve_vpp(G, lS, lG, η=0.8):
    # solver setup
    solver = pulp.PULP_CBC_CMD()
    # parameter setup
    N = len(lS)
    nV = G.number_of_nodes()
    nodes = [v for v in G.nodes()]
    edges = [(u, v) for (u, v) in G.edges()]
    eedges = edges + [(v, u) for (u, v) in G.edges()]
    W = {}
    for (u, v) in edges:
        W[u, v] = W[v, u] = G[u][v]['weight']

    # build model
    m = pulp.LpProblem("VPP", pulp.LpMinimize)

    # 変数定義
    x, b, g, mtz = {}, {}, {}, {}
    for (i, j) in eedges:
        b[i, j] = pulp.LpVariable(f'b_{i}_{j}', 0, 1, 'Binary')
        g[i, j] = pulp.LpVariable(f'g_{i}_{j}', lowBound=0, cat='Continuous')
        m += b[i, j]
        m += g[i, j]
        for k in range(N):
            x[i, j, k] = pulp.LpVariable(f'x({i},{j},{k})', 0, 1, 'Binary')
            m += x[i, j, k]
    for k in range(N):
        for v in nodes:
            mtz[k, v] = pulp.LpVariable(f'mtz({k},{v})', cat='Integer')
            m += mtz[k, v]

    # 制約
    for (i, j) in edges:
        m += pulp.lpSum(x[i, j, k] for k in range(N)) <= N * b[i, j]
        m += pulp.lpSum(x[i, j, k] for k in range(N)) >= b[i, j]
        m += g[i, j] == b[i, j] + η * (pulp.lpSum(x[i, j, n] for n in range(N)) - b[i, j])

    for n in range(N):
        for v in nodes:
            fv = 1 if v == lS[n] else (-1 if v == lG[n] else 0)
            inf = pulp.lpSum(x[v, u, n] for u in G[v])
            ouf = pulp.lpSum(x[u, v, n] for u in G[v])
            m += inf - ouf == fv

    for n in range(N):
        m += mtz[n, lS[n]] == 1
        for (i, j) in eedges:
            if i != lS[n] and j != lS[n] and i != j:
                m += mtz[n, i] - mtz[n, j] + nV * x[i, j, n] <= nV - 1

    # 目的関数
    m += pulp.lpSum(W[u, v] * g[u, v] for (u, v) in eedges)

    # 解く
    m.solve(solver)

    # 解
    obj = pulp.value(m.objective)
    vpp_path = {}
    for n in range(N):
        paths = []
        for (i, j) in eedges:
            if pulp.value(x[i, j, n]) > 0.98:
                paths.append((i, j))
        path = [lS[n]]
        loc = lS[n]
        while loc != lG[n]:
            for (i, j) in paths:
                if i == loc:
                    path.append(j)
                    loc = j
        vpp_path[n] = path

    return obj, vpp_path

if __name__ == '__main__':
    G = pickle.load(open("graph/dataG.pickle", "rb"))
    lS = [1, 2, 3]
    lG = [86] * len(lS)
    obj, paths = solve_vpp(G, lS, lG)
    print(obj)
    for n in range(len(lS)):
        print("{} | {}".format(n, paths[n]))