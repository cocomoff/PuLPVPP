import pickle
import networkx as nx
import matplotlib.pyplot as plt
from vpp import solve_vpp

# read graph from 'random road network generater'
G = pickle.load(open("graph/dataG.pickle", "rb"))
pos = {n: (data['x'], data['y']) for (n, data) in G.nodes(data=True)}

# solve example problem
lS = [1, 2, 3]
lG = [86] * len(lS)
obj, paths = solve_vpp(G, lS, lG)
print(obj)
for n in range(len(lS)):
    print("{} | {}".format(n, paths[n]))

fig = plt.figure(figsize=(5, 5))
ax = fig.gca()
ax.axis("off")
nc, ns = 'gray', 10
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=nc, node_size=ns)
nx.draw_networkx_edges(G, pos, ax=ax, node_color=nc, node_size=ns)

# plot edges
lC = ['r', 'g', 'b']
for n in range(len(lS)):
    path = paths[n]
    for i in range(len(path) - 1):
        pi, pj = path[i:i+2]
        pi, pj = pos[pi], pos[pj]
        print(pi, pj)
        ax.plot([pi[0], pj[0]], [pi[1], pj[1]],
                lw=3, alpha=0.7, color=lC[n])

plt.tight_layout()
plt.savefig("output.png", dpi=72)
plt.close()