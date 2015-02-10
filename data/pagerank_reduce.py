#!/usr/bin/env python

import sys

#
# This program simply represents the identity function.
#
# input of form (node_id, [list of in_ranks])
#               (node_id, '*' + original input line)
node_id = 0
net_rank = 0
input_line = ''
converged = False

for line in sys.stdin:
    split_input = line.partition('\t')
    node_id = split_input[0]
    value = split_input[2]

    # store line input signaled by '*'
    if value.startswith('*'):
        input_line = value[1:]
    else:
        net_rank += int(value)

old_rank = int(input_line.split('\t')[1].split(',')[1])

# scale with alpha
net_rank *= 0.85
# and add small contribution from every other node
net_rank += 0.15

# update input line
node_data = input_line.split('\t')[1].split(',')
# update the old rank to the current rank
node_data[0] = node_data[1]
# update the current rank to the most recently calculated rank
node_data[1] = str(net_rank)
# test for local convergence (no change in rank)
converged = node_data[1] == node_data[0]
input_line = ','.join(node_data)
# re-assemble line
input_line = 'NodeId:' + str(node_id) + '\t' + input_line

sys.stdout.write(converged + '\t' + input_line)
