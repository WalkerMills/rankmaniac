#! /usr/bin/env python

import sys

def main(argv):
    # Flag for specifying if the iteration has converged
    convergance = True
    # Lines that have converged
    final = list()
    # While we have a line to process
    for line in sys.stdin:
        # Strip whitespace
        line = line.rstrip()
        # Extract the key & value from the line
        converged, _, value = line.partition("\t")
        # We got a divergent rank
        if converged == "diverged":
            # Pass the data along to be used for the next iteration
            sys.stdout.write(value + "\n")
        # We got a convergent rank
        elif converged == "converged":
            # Check if this is a null message
            non_null, _, _ = value.partition(",")
            if not non_null:
                # A null converged message indicates global nonconvergence
                convergance = False
                continue
            # If the rankings have not yet diverged
            if convergance:
                # Cache the line while we determine if all nodes have converged
                final.append(value)
            else:
                # Pass the data along to be used for the next iteration
                sys.stdout.write(value + "\n")
    # If all ranks have converged
    if convergance:
        # Output the final rankings
        for line in final:
            node, _, line = line.partition("\t")
            node = node.partition(":")[2]
            line = line.partition(",")[2]
            rank = line.partition(",")[0]
            sys.stdout.write("FinalRank:%s\t%s\n" % (rank, node))

if __name__ == "__main__":
    main(sys.argv)
