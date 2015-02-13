#! /usr/bin/env python

import sys

# Convergence threshold
EPSILON = .002

def main(argv):
    current = dict()
    old = dict()
    children = dict()
    # While we have a line to process
    for line in sys.stdin:
        # sys.stderr.write(line)
        # Strip whitespace
        line = line.rstrip()
        # Extract the key & value from the line
        key, _, value = line.partition("\t")
        # Get the count from the key
        # count, _, _ = key.partition("|")
        # count = int(count)
        # If we got graph structure information
        if value.startswith("*"):
            # Strip the tagging character
            value = value[1:]
            # If this node has converged, we are done
            if value.startswith("C"):
                sys.stdout.write("%s\t%s\n" % (key, value))
                continue
            # The current rank is now the previous rank
            previous, _, data = value.partition(",")
            old[key] = float(previous)
            # Ignore the rank before the now previous rank, store the children
            _, _, children[key] = data.partition(",")
        else:
            # Otherwise, we got a rank contribution
            try:
                current[key] += float(value)
            except KeyError:
                current[key] = float(value)
    for key, previous in old.items():
        # Update this node's rank
        try:
            rank = 0.85 * current[key] + 0.15
        except KeyError:
            rank = 0.15
        # Write the updated line, along with a convergence flag
        sys.stdout.write("%s\t%s%f,%f,%s\n" %
            (key, "C," * (abs(rank - previous) / rank <= EPSILON), rank,
             previous, children[key]))

if __name__ == "__main__":
    main(sys.argv)
