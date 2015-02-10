#!/usr/bin/env python

import sys

#
# **should be passing either (node, rank_contribution)
#                            (node, input line)

for line in sys.stdin:
    # set the node id
    node_id = line.partition(':')[2].rpartition('\t')[0]
    # separate data
    data = line.split('\t')
    # get ranks of node from data
    current_rank = int(data[0].split(',')[0])
    old_rank = int(data[0].split(',')[1])
    # get neighboring nodes from data
    neighbors = data[1].split(',')

    for node in neighbors:
        rank_cmpnt = current_rank / len(neighbors)
        sys.stdout.write(node + '\t' + rank_cmpnt)

    # pass 
    # pass input so that it can be used on next iteration
    sys.stdout.write(node_id + '\t' + '*' + line)