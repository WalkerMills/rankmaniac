#! /usr/bin/env python

import sys

def main(argv):
    updates = dict()
    # While we have a line to process
    for line in sys.stdin:
        # Strip whitespace
        line = line.rstrip()
        # Extract the key & value from the line
        key, _, value = line.partition("\t")
        # Initialize count
        count = int()
        # update count, or add a spot for the count if it's the first iteration
        if key.startswith("N"):
            count = 1
        else:
            count, _, key = key.partition("_")
            count = int(count) + 1
        key = str(count) + "_" + key
        # Continue passing local graph information
        sys.stdout.write("%s\t*%s\n" % (key, value))
        # Remove power_ext to isolate children
        data = value.partition(';')[0]
        # Parse data in the form (C,)?current_rank,old_rank,children
        data = data.split(",")
        # Check for convergence
        converged = data[0] == "C"
        # Slice the converged flag off the data, if it exists
        data = data[converged:]
        # Get this node's current rank
        current = float(data[0])

        try:
            # Cast the children's indices to integers
            children = [int(n) for n in data[2:]]
            # Distribute the rank of this node among its children
            inheritance = current / len(children)
        # If this node has no children
        except (ValueError, ZeroDivisionError):
            # And it has not yet converged
            if not converged:
                # Give this node all of its rank in the next iteration
                sys.stdout.write("%s\t%f\n" % (key, current))
            continue
        # Aggregate the children's ranks locally
        for node in children:
            try:
                updates[node] += inheritance
            except KeyError:
                updates[node] = inheritance
    # Emit the aggregated ranks
    for node, inheritance in updates.items():
        sys.stdout.write("%d_NodeId:%s\t%f\n" % (count, node, inheritance))

if __name__ == "__main__":
    main(sys.argv)
