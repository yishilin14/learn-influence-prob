#!/usr/bin/env python
import csv
import sys

# input: digg_friends.csv
# output grpah.txt
print("digg_friends.csv -> graph.txt")
fin_link = open('raw/digg_friends.csv')
fout_graph = open("learn/graph_dir.txt", "w")
fout_graph_un = open("learn/graph_undir.txt", "w")
user_set = set()
num_edges = 0
for row in csv.reader(fin_link):
    mutual = int(row[0])
    timestamp = int(row[1])
    u = int(row[2])
    v = int(row[3])
    user_set.add(u)
    user_set.add(v)
    num_edges = num_edges + 1
    fout_graph.write("%d %d %d\n" % (u, v, timestamp))
    fout_graph_un.write("%d %d %d\n" % (u, v, timestamp))
    if mutual == 1:
        fout_graph.write("%d %d %d\n" % (v, u, timestamp))
fin_link.close()
fout_graph.close()
fout_graph_un.close()
print("Number of users: ", len(user_set))
print("Number of directed edges: ", num_edges)

# input: votes.timed.txt
# output: action_logs.txt
print("digg_votes1.csv -> action_logs.txt")
fin_vote = open("raw/digg_votes1.csv", "r")
story_set = set()
action_logs = []
user_set = set()
for row in csv.reader(fin_vote):
    timestamp = row[0]
    user = row[1]
    story = row[2]
    story_set.add(story)
    user_set.add(user)
    action_logs.append([user, story, timestamp])
fin_vote.close()
print("Number of action logs: ", len(action_logs))
print("Number of stories: ", len(story_set))
print("Number of users voted: ", len(user_set))

# Sort action logs and output
print("Sorting action_logs...")
action_logs = sorted(action_logs, key = lambda t:(t[1],t[0],t[2]))
print("Writing action_logs...")
fout_action = open("learn/action_logs.txt", "w")
for line in action_logs:
    fout_action.write("%s %s %s\n" % (line[0], line[1], line[2]))
fout_action.close()

# Output all action-ids
fout_actionid = open("learn/action_ids.txt", "w")
for id in story_set:
    fout_actionid.write("%s\n" % id)
fout_actionid.close()
