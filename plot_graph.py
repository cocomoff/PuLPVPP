import pickle
import networkx as nx
import matplotlib.pyplot as plt

# read graph from 'random road network generater'
G = pickle.load(open("graph/dataG.pickle", "rb"))
pos = {n: (data['x'], data['y']) for (n, data) in G.nodes(data=True)}

fig = plt.figure(figsize=(5, 5))
ax = fig.gca()
ax.axis("off")
nc, ns = 'blue', 20
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=nc, node_size=ns)
nx.draw_networkx_edges(G, pos, ax=ax, node_color=nc, node_size=ns)
plt.tight_layout()
plt.show()
plt.close()