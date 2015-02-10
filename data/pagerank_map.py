#!/usr/bin/env python2

import sys

def main(argv):
    # While we have a line to process
    for line in sys.stdin:
        # Strip whitespace
        line = line.rstrip()
        # Extract the key & value from the line
        key, _, value = line.partition("\t")
        # Parse data in the form current_rank,old_rank,children
        data = value.split(",")
        current = float(data[0])
        try:
            children = [int(n) for n in data[2:]]
        except ValueError:
            children = list()
        try:
            # Distribute the rank of this node among its children
            inheritance = current / len(children)
            for node in children:
                sys.stdout.write("NodeId:{}\t{}\n".format(node, inheritance))
        except ZeroDivisionError:
            pass
        # Continue passing local graph information
        sys.stdout.write("{}\t*{}\n".format(key, value))

if __name__ == "__main__":
    main(sys.argv)
