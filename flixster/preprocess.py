#!/usr/bin/env python
import time
from datetime import date, datetime
from igraph import *

# Input: links.txt (undirected)
# Output grpah.txt
# Read the graph
g = Graph.Read_Edgelist("raw/links.txt", directed=False)
print("Number of nodes: ", g.vcount())
print("Number of undirected edges: ", g.ecount())
# Simplify
g = g.simplify()
g.es["weight"] = 0  # dummy weight
print("After simplify:")
print("Number of nodes: ", g.vcount())
print("Number of undirected edges: ", g.ecount())
# Output the undirected graph (with weights)
g.write_ncol("learn/graph_undir.txt", names=None)
g.to_directed(mutual=True)
# Output the directed graph (with weights)
print("Number of directed edges: ", g.ecount()) 
g.write_ncol("learn/graph_dir.txt", names=None)

# Input: ratings.timed.txt
# Output: actions.txt
fin_rating = open("raw/ratings.timed.txt", "r")
line = fin_rating.readline()  # skip the first line
movie_set = set()
action_logs = []
for line in fin_rating:
    arr = line.replace('\00', '').split()
    if len(arr) == 5 :
        user = int(arr[0])
        movie = int(arr[1])
        movie_set.add(movie)
        timestamp = int(datetime.strptime(arr[3], '%Y-%m-%d').strftime("%s"))
        action_logs.append([user, movie, timestamp])
fin_rating.close()
print("Number of logs: ", len(action_logs))
print("Number of action ids: ", len(movie_set))

# Sort action logs and output
print("Sorting action_logs...")
action_logs = sorted(action_logs, key = lambda t:(t[1],t[0],t[2]))
print("Writing action_logs...")
with open("learn/action_logs.txt", "w") as fout_action:
    for line in action_logs:
        if line[2] > 1000000000:
            fout_action.write("%d %d %d\n" % (line[0], line[1], line[2]))

# Output all action-ids
with open("learn/action_ids.txt", "w") as fout_actionid:
    for id in movie_set:
        fout_actionid.write("%d\n" % id)
