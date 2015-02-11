#! /usr/bin/env python

import sys

def main(argv):
    # Flag for specifying if the iteration has converged
    convergence = True
    # Lines that have converged
    final = list()
    # While we have a line to process
    for line in sys.stdin:
        # sys.stderr.write(line)
        # Strip whitespace
        line = line.rstrip()
        # Extract the key & value from the line
        converged, _, value = line.partition("\t")
        # We got a divergent rank
        if converged == "diverged":
            # Pass the data along to be used for the next iteration
            sys.stdout.write(value + "\n")
            convergence = False
        # We got a convergent rank
        elif converged == "converged":
            # If the rankings have not yet diverged
            if convergence:
                # Cache the line while we determine if all nodes have converged
                final.append(value)
            else:
                # Pass the data along to be used for the next iteration
                sys.stdout.write(value + "\n")
    # If all ranks have converged
    if convergence:
        # Output the final rankings
        for line in final:
            node, _, line = line.partition("\t")
            node = node.partition(":")[2]
            line = line.partition(",")[2]
            rank = line.partition(",")[0]
            sys.stdout.write("FinalRank:%s\t%s\n" % (rank, node))
    else:
        for line in final:
            sys.stdout.write(line + "\n")

if __name__ == "__main__":
    main(sys.argv)
