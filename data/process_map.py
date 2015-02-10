#!/usr/bin/env python

import sys

#
# Reads the output from pagerank_reduce. Determines if a node has
# converged (no change in rank) and emits corresponding information
#
# input is either   (converged flag, input_line)
for line in sys.stdin:
    converged, input_line = line.partition('\t')
    if converged:
        sys.stdout.write(line)
    else:
        sys.stdout.write(line)
        # when reducer for not converged comes across '*', it knows
        # that not all of the nodes have converged
        sys.stdout.write('True' + '\t' + '*')
