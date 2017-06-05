#!/usr/bin/env python
import time
from datetime import date, datetime
from igraph import *

link_filename = "raw/flickr-growth.txt"
action_filename = "raw/flickr-all-photo-favorite-markings.txt"

# Input: links.txt (undirected)
# Output grpah.txt
# Read the graph
print("Get graph.txt")
fin_link = open(link_filename, "r")
fout_graph = open("learn/graph_dir.txt", "w")
user_set = set()
num_edges = 0
for line in fin_link:
   line = line.split()
   u = int(line[0])
   v = int(line[1])
   user_set.add(u)
   user_set.add(v)
   num_edges = num_edges + 1
   fout_graph.write("%d %d 0\n" % (u, v))
fin_link.close()
fout_graph.close()
print("Number of users: ", len(user_set))
print("Number of directed edges: ", num_edges)

# Input: ratings.timed.txt
# Output: actions.txt
fin_rating = open(action_filename, "r")
photo_set = set()
action_logs = []
for line in fin_rating:
    arr = line.split()
    if len(arr) == 3 :
        user = int(arr[0])
        photo = int(arr[1])
        photo_set.add(photo)
        timestamp = int(arr[2])
        action_logs.append([user, photo, timestamp])
    else :
        print(arr)
fin_rating.close()
print("Number of logs: ", len(action_logs))
print("Number of action ids: ", len(photo_set))

# Sort action logs and output
print("Sorting action_logs...")
action_logs.sort(key = lambda t:(t[1],t[0],t[2]))
print("Writing action_logs...")
with open("learn/action_logs.txt", "w") as fout_action:
    for line in action_logs:
        fout_action.write("%d %d %d\n" % (line[0], line[1], line[2]))

# Output all action-ids
with open("learn/action_ids.txt", "w") as fout_actionid:
    for id in photo_set:
        fout_actionid.write("%d\n" % id)
