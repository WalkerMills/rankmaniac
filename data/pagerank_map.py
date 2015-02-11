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
        # Continue passing local graph information
        sys.stdout.write("%s\t*%s\n" % (key, value))
        # Parse data in the form current_rank,old_rank,children
        data = value.split(",")
        current = data[0]
        # If this node's rank has converged
        if current.startswith("C"):
            # Give this node all of its rank in the next iteration
            sys.stdout.write("%s\t*%s\n" % (key, value))
            # Stop processing this node
            continue
        current = float(current)
        try:
            children = [int(n) for n in data[2:]]
            # Distribute the rank of this node among its children
            inheritance = current / len(children)
            # Aggregate the children's ranks locally
            for node in children:
                try:
                    updates[node] += inheritance
                except KeyError:
                    updates[node] = inheritance
        # If this node has no children
        except (ValueError, ZeroDivisionError):
            # Give this node all of its rank in the next iteration
            sys.stdout.write("%s\t%f\n" % (key, current))
    # Emit the aggregated ranks
    for node, inheritance in updates.items():
        sys.stdout.write("NodeId:%s\t%f\n" % (node, inheritance))

if __name__ == "__main__":
    main(sys.argv)
