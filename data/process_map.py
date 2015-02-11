#! /usr/bin/env python

import sys

def main(argv):
    # While we have a line to process
    for line in sys.stdin:
        # Strip whitespace
        line = line.rstrip()
        # Extract the key & value from the line
        key, _, value = line.partition("\t")
        # Extract the convergence flag
        converged, _, value = value.partition(",")
        # If the ranks for this node converged
        if converged:
            # Send this node to the converged reducer
            sys.stdout.write("converged\t%s\tC,%s\n" % (key, value))
        else:
            # Send a null message to the converged reducer
            sys.stdout.write("converged\t,\n")
            # Send this node to the diverged reducer
            sys.stdout.write("diverged\t%s\t%s\n" % (key, value))

if __name__ == "__main__":
    main(sys.argv)
