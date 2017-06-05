#!/usr/bin/env python
import csv
import sys
from io import StringIO
import re

# input: active_follower_real.sql
# output grpah.txt
print("active_follower_real.sql -> graph.txt")
# input
dump_filename = 'raw/active_follower_real.sql'
target_table = 'active_follower_real'
# output
fout_graph = open("learn/graph_dir.txt", "w")
# input -> output
fast_forward = True
user_set = set()
num_edges = 0
with open(dump_filename, 'r') as f:
    for line in f:
        line = line.strip()
        if line.lower().startswith('insert') and target_table in line:
            fast_forward = False
        if fast_forward:
            continue
        data = re.findall('\([^\)]*\)', line)
        for newline in data:
            newline = newline.strip(' ()')
            newline = newline.replace('`', '')
            newline = newline.replace(',', ' ')
            newline = newline.split()
            if newline[0].isdigit() and newline[1].isdigit():
                # follower (newline[1]) -> user (newline[0])
                fout_graph.write("%s %s 0\n" % (newline[1], newline[0]))
                user_set.add(newline[0])
                user_set.add(newline[1])
                num_edges = num_edges + 1
fout_graph.close()
print("Number of users: ", len(user_set))
print("Number of links: ", num_edges)

# input: votes.timed.txt
# output: actions.txt
print("raw/link_status_search_with_ordering_real.csv -> action.txt")
fin_vote = open("raw/link_status_search_with_ordering_real.csv", "r")
url_dict = {}
num_url = 0
action_logs = []
reader = csv.reader(fin_vote)
next(reader, None) # skip the headers
for row in reader:
    url = row[0].strip()
    timestamp = int(row[-2])
    user = int(row[-1])
    if url_dict.get(url) == None:
        num_url = num_url + 1;
        url_dict[url] = num_url
        url_id = num_url
    else:
        url_id = url_dict[url]
    action_logs.append([user, url_id, timestamp])
fin_vote.close()
print("Number of action logs: ", len(action_logs))
print("Number of url: ", num_url)

# Sort action logs and output
print("Sorting action_logs...")
action_logs = sorted(action_logs, key = lambda t:(t[1],t[0],t[2]))
print("Writing action_logs...")
fout_action = open("learn/action_logs.txt", "w")
last_line = (-1, -1, -1)
skip = 0
for line in action_logs:
    # If a user tweets a url multiple times, we only keep the smallest timestamp.
    if line[0]!=last_line[0] or line[1]!=last_line[1]:
        fout_action.write("%d %d %d\n" % (line[0], line[1], line[2]))
        last_line = line
    else:
        skip = skip + 1
fout_action.close()
print("Skip ", skip, "logs")

# Output all action-ids
fout_actionid = open("learn/action_ids.txt", "w")
for id in (range(1,num_url+1)):
    fout_actionid.write("%s\n" % id)
fout_actionid.close()
