#!/usr/bin/env python
from igraph import *

# Read the directed graph (output of preprocess.py)
g = Graph.Read_Ncol("learn/graph_dir.txt", directed=True)
print("Number of nodes: ", g.vcount())
print("Number of directed edges: ", g.ecount())
g = g.simplify()
print("[Simplify] Number of nodes: ", g.vcount())
print("[Simplify] Number of directed edges: ", g.ecount())
g.es["weight"] = 0.0

# Read actions performed by each user
print("Loading usersCounts...")
f_nodes = open("learn/usersCounts.txt", "r")
user_action = {}
for line in f_nodes:
    v, a_v = [int(x) for x in line.split()]
    user_action[v] = a_v
f_nodes.close()

# Read edges, and replace the weights in g by influence probabilities
print("Loading edgesCounts...")
f_edges = open("learn/edgesCounts.txt", "r")
for line in f_edges:
    line = line.split()
    u, v, a_u2v, a_v2u = [int(x) for x in line[0:4]]
    if u in user_action.keys() and v in user_action.keys():
        # u -> v
        uid = g.vs.find(str(u))
        vid = g.vs.find(str(v))
        eid_uv = g.get_eid(uid, vid, error=False)
        if eid_uv >=0 and user_action[u] > 0:
            g.es[eid_uv]["weight"] = round(float(a_u2v) / user_action[u], 6)
        # v -> u
        eid_vu = g.get_eid(vid, uid, error=False)
        if eid_vu >= 0 and user_action[v] > 0:
            g.es[eid_vu]["weight"] = round(float(a_v2u) / user_action[v], 6)
f_edges.close()

# Delete edges with zero influence probabilities
g.delete_edges(g.es.select(weight_le=0))
print("Number of edges after deletion: ", g.ecount())

lwcc = g.clusters(mode='weak').giant()
lwcc.vs["name"] = range(lwcc.vcount())
print("Largest weakly connected component")
print("Number of nodes: ", lwcc.vcount(), float(lwcc.vcount()) / g.vcount())
print("Number of directed edges: ", lwcc.ecount())

# Output to files
with open("digg_learn/attribute.txt", "w") as f_attr:
    f_attr.write("n=%d" % lwcc.vcount())
    f_attr.write("m=%d" % lwcc.ecount())

lwcc.write_ncol("digg_learn/graph_ic.inf")
with open("digg_learn/graph_ic_nm.inf", "w") as f_graph_nm:
    f_graph_nm.write("%d %d\n" % (lwcc.vcount(), lwcc.ecount()))
    with open("digg_learn/graph_ic.inf", "r") as f_tmp:
        f_graph_nm.write(f_tmp.read())
