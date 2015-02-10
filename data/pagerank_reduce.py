#!/usr/bin/env python2

import sys

def main(argv):
    key = str()
    current = float()
    old = float()
    children = str()
    # While we have a line to process
    for line in sys.stdin:
        # Strip whitespace
        line = line.rstrip()
        # Extract the key & value from the line
        key, _, value = line.partition("\t")
        # If we got graph structure information
        if value.startswith("*"):
            # The current rank is now the previous rank
            old, _, data = value[1:].partition(",")
            old = float(old)
            # Ignore the rank before the now previous rank, store the children
            _, _, children = data.partition(",")
        else:
            # Otherwise, we got a rank contribution
            current += float(value)
    # Scale the new rank with alpha, and add 1 - alpha
    current = 0.85 * current + 0.15
    # Write the updated line, along with a convergence flag
    sys.stdout.write("{}\t{},{},{},{}\n".format(
        key, "C" * (abs(current - old) <= .0025), current, old, children))

if __name__ == "__main__":
    main(sys.argv)
